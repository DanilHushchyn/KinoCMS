"""Schemas for mailing"""

import ninja_schema
from django.utils.translation import gettext as _
from ninja import ModelSchema
from pydantic import field_validator

from config.settings.settings import ABSOLUTE_URL
from src.core.errors import NotFoundExceptionError
from src.mailing.models import MailTemplate


class MailTemplateOutSchema(ModelSchema):
    """Pydantic schema for MailTemplate.

    Purpose of this schema to return mail template data
    """

    @staticmethod
    def resolve_file(obj: MailTemplate):
        return ABSOLUTE_URL + str(obj.file.url)

    class Meta:
        model = MailTemplate
        fields = [
            "id",
            "name",
        ]


class MailingInSchema(ninja_schema.Schema):
    """Pydantic schema for mailing.

    Purpose of this schema to make mailing
    """

    user_ids: list[int] = None
    temp_id: int

    @field_validator("temp_id")
    def clean_recipients(cls, temp_id: int) -> int:
        try:
            MailTemplate.objects.get(id=temp_id)
        except MailTemplate.DoesNotExist:
            msg = _("Не знайдено: немає збігів шаблонів " "на заданному запиті")
            raise NotFoundExceptionError(message=msg, cls_model=MailTemplate)
        return temp_id


class TaskInfoOutSchema(ninja_schema.Schema):
    """Pydantic schema for getting task info.

    Purpose of this schema to get task info
    """

    progress: int
    letters_count: int
