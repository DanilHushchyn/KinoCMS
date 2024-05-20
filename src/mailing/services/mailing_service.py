import re
from typing import List

import loguru
from django.core.exceptions import ValidationError
from django.db.models import Q, QuerySet
from ninja.errors import HttpError
from django.utils.translation import gettext as _
from ninja import File
from ninja.files import UploadedFile
from src.core.schemas import MessageOutSchema
from src.core.utils import paginate
from src.mailing.models import MailTemplate
from src.users.models import User


class MailingService:
    """
    A service class for mailing.
    """

    @staticmethod
    def send_mail(user_id: int) -> User:
        """
        Get user personal data by id.

        :param user_id: user id
        :return: User model instance
        """
        user = User.objects.get_by_id(user_id)
        return user

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
