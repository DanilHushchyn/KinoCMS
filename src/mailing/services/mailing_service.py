import loguru
from celery.result import AsyncResult
from django.db.models import QuerySet
from ninja.errors import HttpError
from django.utils.translation import gettext as _
from ninja import File
from ninja.files import UploadedFile
from django.core.cache import cache

from src.core.schemas.base import MessageOutSchema
from src.mailing.models import MailTemplate
from src.mailing.schemas import MailingInSchema
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
        # inspector = app.control.inspect()
        # actives = 0
        # for key, value in inspector.active().items():
        #     actives = len(value)
        if cache.get(f'mailing_task') is None:
            task = make_mailing.delay(users_list=body.users,
                                      temp_id=body.temp_id)
            cache.set(f'mailing_task', task.id)
        else:
            msg = _('Треба зачекати поки закінчиться поточне розсилання')
            raise HttpError(400, msg)
        return MessageOutSchema(detail=_('Розсилання почалося'))

    @staticmethod
    def get_task_info() -> dict:
        """
        Get templates for mailing.

        :return: MailTemplate QuerySet
        """
        # inspector = app.control.inspect()
        # current_task_id = None
        # for key, tasks in inspector.active().items():
        #     for task in tasks:
        #         current_task_id = task['id']
        # print(current_task_id)
        task_id = cache.get(f'mailing_task')
        if task_id:
            task = AsyncResult(task_id)
            data = task.result
            result = (data['current'] / data['total']) * 100
            loguru.logger.debug(data)
        else:
            msg = _('На теперішній час розсилання не активне')
            raise HttpError(400, msg)
        return {
            'progress': int(result)
        }

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
            raise HttpError(403, msg)
        if file.size > 1_000_000:
            msg = _('Максимально дозволений розмір файлу 1MB')
            raise HttpError(403, msg)
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
            raise HttpError(404, msg)
        template.delete()
        return MessageOutSchema(detail=_('Шаблон успішно видалений'))
