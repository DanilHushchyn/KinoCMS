from celery.result import AsyncResult
from django.db.models import QuerySet
from django.utils.translation import gettext as _
from ninja import File
from ninja.files import UploadedFile
from django.core.cache import cache

from src.core.errors import UnprocessableEntityExceptionError, NotFoundExceptionError
from src.core.schemas.base import MessageOutSchema
from src.mailing.errors import MailingIsActiveExceptionError, MailingIsNotActiveExceptionError
from src.mailing.models import MailTemplate
from src.mailing.schemas import MailingInSchema, TaskInfoOutSchema
from src.mailing.tasks import make_mailing


class MailingService:
    """
    A service class for mailing.
    """

    @staticmethod
    def send_mail(body: MailingInSchema) -> MessageOutSchema:
        """
        Get user personal data by id.

        :param body: contains data
        (template's id for mailing, list of recipients)
        for mailing
        :return: message that everything is ok and mailing started
        """
        if cache.get(f'mailing_task') is None:
            temp = MailTemplate.objects.get(id=body.temp_id)
            with open(f'{temp.file.path}', 'r') as file:
                html_content = file.read()
            task = make_mailing.delay(user_ids=body.user_ids,
                                      html_content=html_content)
            cache.set(f'mailing_task', task.id)
        else:
            msg = _('Треба зачекати поки закінчиться поточне розсилання')
            raise MailingIsActiveExceptionError(message=msg)
        return MessageOutSchema(detail=_('Розсилання почалося'))

    @staticmethod
    def get_task_info() -> int and MessageOutSchema | dict[str, int]:
        """
        Get templates for mailing.

        :return: MailTemplate QuerySet
        """
        task_id = cache.get(f'mailing_task')
        if task_id:
            task = AsyncResult(task_id)
            if task.result == 'COMPLETE':
                cache.delete(f'mailing_task')
                msg = _('Розсилання успішно виконане')
                return 201, MessageOutSchema(detail=msg)
            data = task.result
            result = (data['current'] / data['total']) * 100
            return 200, TaskInfoOutSchema(progress=int(result))
        else:
            msg = _('На теперішній час розсилання не активне')
            raise MailingIsNotActiveExceptionError(message=msg)


    @staticmethod
    def get_templates() -> QuerySet:
        """
        Get templates for mailing.

        :return: MailTemplate QuerySet
        """
        templates = MailTemplate.objects.all()[:5]
        return templates

    @staticmethod
    def create_template(file: UploadedFile = File(...)) -> MailTemplate:
        """
        Create template for mailing.
        """
        if file.content_type != 'text/html':
            msg = _('Дозволено відправляти тільки html')
            raise UnprocessableEntityExceptionError(message=msg)
        if file.size > 1_000_000:
            msg = _('Максимально дозволений розмір файлу 1MB')
            raise UnprocessableEntityExceptionError(message=msg)
        name = file.name.split('.')[0]
        template = MailTemplate.objects.create(file=file, name=name)
        return template

    @staticmethod
    def delete_template(temp_id: int) -> MessageOutSchema:
        """
        Delete template for mailing by id.

        :return: message about operation status
        """
        try:
            template = MailTemplate.objects.get(id=temp_id)
        except MailTemplate.DoesNotExist:
            msg = _('Не знайдено: немає збігів шаблонів '
                    'на заданному запиті')
            raise NotFoundExceptionError(message=msg, cls_model=MailTemplate)
        task_id = cache.get(f'mailing_task')
        if task_id:
            msg = _('Треба зачекати поки закінчиться поточне розсилання')
            raise MailingIsActiveExceptionError(message=msg)
        template.delete()
        return MessageOutSchema(detail=_('Шаблон успішно видалений'))
