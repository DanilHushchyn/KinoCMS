from celery.result import AsyncResult
from django.core.cache import cache
from django.db.models import QuerySet
from django.utils.translation import gettext as _
from ninja import File
from ninja.files import UploadedFile

from src.core.errors import NotFoundExceptionError
from src.core.errors import UnprocessableEntityExceptionError
from src.core.schemas.base import MessageOutSchema
from src.mailing.errors import MailingIsActiveExceptionError
from src.mailing.models import MailTemplate
from src.mailing.schemas import MailingInSchema
from src.mailing.schemas import TaskInfoOutSchema
from src.mailing.tasks import make_mailing


class MailingService:
    """A service class for mailing."""

    @staticmethod
    def send_mail(body: MailingInSchema) -> MessageOutSchema:
        """Get user personal data by id.

        :param body: contains data
        (template's id for mailing, list of recipients)
        for mailing
        :return: message that everything is ok and mailing started
        """
        if cache.get("mailing_task") is None:
            temp = MailTemplate.objects.get(id=body.temp_id)
            with open(f"{temp.file.path}") as file:
                html_content = file.read()
            task = make_mailing.delay(user_ids=body.user_ids, html_content=html_content)
            cache.set("mailing_task", task.id)
        else:
            msg = _("Треба зачекати поки закінчиться поточне розсилання")
            raise MailingIsActiveExceptionError(message=msg)
        return MessageOutSchema(detail=_("Розсилання почалося"))

    @staticmethod
    def get_task_info() -> int and MessageOutSchema | dict[str, int]:
        """Get templates for mailing.

        :return: MailTemplate QuerySet
        """
        task_id = cache.get("mailing_task")
        if task_id:
            task = AsyncResult(task_id)
            if task.result == "COMPLETE":
                cache.delete("mailing_task")
                msg = _("Розсилання успішно виконане")
                return 201, MessageOutSchema(detail=msg)
            data = task.result
            current = 0
            total = 100
            if isinstance(data, dict):
                current = data["current"]
                total = data["total"]
            result = (current / total) * 100
            return 200, TaskInfoOutSchema(
                progress=int(result), letters_count=int(total)
            )
        else:
            msg = _("На теперішній час розсилання не активне")
            return 202, MessageOutSchema(detail=msg)

    @staticmethod
    def get_templates() -> QuerySet:
        """Get templates for mailing.

        :return: MailTemplate QuerySet
        """
        templates = MailTemplate.objects.all()[:5]
        return templates

    @staticmethod
    def create_template(file: UploadedFile = File(...)) -> MailTemplate:
        """Create template for mailing."""
        print(file.content_type)
        if file.content_type != "text/html":
            msg = _("Дозволено відправляти тільки html")
            raise UnprocessableEntityExceptionError(message=msg)
        if file.size > 1_000_000:
            msg = _("Максимально дозволений розмір файлу 1MB")
            raise UnprocessableEntityExceptionError(message=msg)
        name = file.name.split(".")[0]
        template = MailTemplate.objects.create(file=file, name=name)
        return template

    @staticmethod
    def delete_template(temp_id: int) -> MessageOutSchema:
        """Delete template for mailing by id.

        :return: message about operation status
        """
        try:
            template = MailTemplate.objects.get(id=temp_id)
        except MailTemplate.DoesNotExist:
            msg = _("Не знайдено: немає збігів шаблонів " "на заданному запиті")
            raise NotFoundExceptionError(message=msg, cls_model=MailTemplate)
        task_id = cache.get("mailing_task")
        if task_id:
            msg = _("Треба зачекати поки закінчиться поточне розсилання")
            raise MailingIsActiveExceptionError(message=msg)
        template.delete()
        return MessageOutSchema(detail=_("Шаблон успішно видалений"))
