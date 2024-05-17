# -*- coding: utf-8 -*-
"""
    Module contains class for managing users data in the site.

"""
import re

import loguru
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpRequest
from ninja.errors import HttpError
from django.utils.translation import gettext as _

from src.core.schemas import MessageOutSchema
from src.core.utils import paginate
from src.users.models import User
from src.users.schemas import UserRegisterSchema, UserUpdateSchema
from phonenumber_field.validators import validate_international_phonenumber


class UserService:
    """
    A service class for managing users.
    """

    @staticmethod
    def get_by_id(user_id: int) -> User:
        """
        Get user personal data by id.

        :param user_id: user id
        :return: User model instance
        """
        user = User.objects.get_by_id(user_id)
        return user

    @staticmethod
    def delete_by_id(user_id: int) -> MessageOutSchema:
        """
        Get user personal data by id.

        :param user_id: user id
        :return: User model instance
        """
        result = User.objects.delete_by_id(user_id)
        return result

    @staticmethod
    def validate_fio(fio: str) -> bool:
        pattern = r"^[А-ЯЇІЄҐ][а-яїієґ'-]+$"
        if fio is None or re.match(pattern, fio):
            return True
        else:
            return False

    def register(self, user_body: UserRegisterSchema) -> MessageOutSchema:
        """
        Get user personal data by id.

        :param user_body: user's personal data
        :return: info about registration status
        """
        try:
            validate_international_phonenumber(user_body.phone_number)
        except ValidationError:
            raise HttpError(403, _("Введено некоректний номер телефону."))
        if not self.validate_fio(user_body.first_name):
            msg = _("Ім'я повинно починатися з великої літери"
                    "(наступні маленькі), доступна кирилиця, "
                    "доступні спецсимволи('-)")
            raise HttpError(403, msg)
        if not self.validate_fio(user_body.last_name):
            msg = _("Прізвище повинно починатися з великої літери"
                    "(наступні маленькі), доступна кирилиця, "
                    "доступні спецсимволи('-)")
            raise HttpError(403, msg)
        User.objects.register(user_body=user_body)
        msg = _("Ви успішно зареєструвалися")
        return MessageOutSchema(message=msg)

    def update_by_id(self, user_id: int, user_body: UserUpdateSchema) \
            -> User:
        """
        Get user personal data by id.

        :param user_id: user's model instance id
        :param user_body: user's personal data
        :return: info about registration status
        """
        try:
            phone = user_body.phone_number
            if phone is not None and not phone:
                raise ValidationError('')
            validate_international_phonenumber(user_body.phone_number)
        except ValidationError:
            raise HttpError(403, _("Введено некоректний номер телефону."))
        if not self.validate_fio(user_body.first_name):
            msg = _("Ім'я повинно починатися з великої літери"
                    "(наступні маленькі), доступна кирилиця, "
                    "доступні спецсимволи('-)")
            raise HttpError(403, msg)
        if not self.validate_fio(user_body.last_name):
            msg = _("Прізвище повинно починатися з великої літери"
                    "(наступні маленькі), доступна кирилиця, "
                    "доступні спецсимволи('-)")
            raise HttpError(403, msg)
        user = User.objects.update_by_id(user_id=user_id,
                                         user_body=user_body)
        return user

    @staticmethod
    def get_all(page: int, page_size: int) -> dict:
        """
        Get all users.

        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :return: dict which contains all parameters for pagination
        """
        users = User.objects.all()
        return paginate(items=users, page=page, page_size=page_size)

    @staticmethod
    def search(search_line: str, page: int, page_size: int) -> dict:
        """
        Get all users.

        :param search_line: line for searching users
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :return: dict which contains all parameters for pagination
        """
        users = User.objects.filter(
            Q(id__icontains=search_line) |
            Q(first_name__icontains=search_line) |
            Q(last_name__icontains=search_line) |
            Q(email__icontains=search_line) |
            Q(nickname__icontains=search_line) |
            Q(phone_number__icontains=search_line) |
            Q(date_joined__icontains=search_line) |
            Q(birthday__icontains=search_line)
        )
        return paginate(items=users, page=page, page_size=page_size)
    #
    # @staticmethod
    # def get_my_profile(user_id: int) -> User:
    #     """
    #     Get user personal data by id.
    #
    #     :param user_id: user id
    #     :return: User model instance
    #     """
    #     try:
    #         user = User.objects.get(id=user_id)
    #     except User.DoesNotExist:
    #         raise HttpError(404,
    #                         _("Not Found: No User matches"
    #                           " the given query."))
    #     return user
