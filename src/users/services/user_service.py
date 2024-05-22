# -*- coding: utf-8 -*-
"""
    Module contains class for managing users data in the site.

"""
import re
from typing import List

import loguru
from django.core.exceptions import ValidationError
from django.db.models import Q
from ninja.errors import HttpError
from django.utils.translation import gettext as _

from src.core.schemas.base import MessageOutSchema
from src.core.utils import paginate
from src.users.models import User
from src.users.schemas import UserRegisterSchema, UserUpdateSchema, UserFieldsEnum


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
    def get_cities() -> List:
        """
        Get user's choices for cities.

        :return: list of cities
        """
        cities = User.CITIES_CHOICES
        return cities

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
    def register(user_body: UserRegisterSchema) -> MessageOutSchema:
        """
        Get user personal data by id.

        :param user_body: user's personal data
        :return: info about registration status
        """
        User.objects.register(user_body=user_body)
        msg = _("Ви успішно зареєструвалися")
        return MessageOutSchema(detail=msg)

    @staticmethod
    def update_by_id(user_id: int, user_body: UserUpdateSchema) \
            -> User:
        """
        Get user personal data by id.

        :param user_id: user's model instance id
        :param user_body: user's personal data
        :return: info about registration status
        """
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
    def search(search_line: str, sort: UserFieldsEnum, ascending: bool,
               page: int, page_size: int) -> dict:
        """
        Get all users.

        :param ascending: value about how to order users
        by ascending or by descending
        :param sort: parameter for sorting
        :param search_line: line for searching users
        :param page: the page number we want to get
        :param page_size: length of queryset per page
        :return: dict which contains all parameters for pagination
        """
        users = User.objects.all()
        if search_line:
            users = users.filter(
                Q(id__icontains=search_line) |
                Q(first_name__icontains=search_line) |
                Q(last_name__icontains=search_line) |
                Q(email__icontains=search_line) |
                Q(nickname__icontains=search_line) |
                Q(phone_number__icontains=search_line) |
                Q(date_joined__icontains=search_line) |
                Q(birthday__icontains=search_line) |
                Q(city__icontains=search_line)
            )
        if sort:
            symbol = '' if ascending else '-'
            if sort.name == 'fio':
                users = users.order_by(f'{symbol}last_name',
                                       f'{symbol}first_name')
            else:
                users = users.order_by(f'{symbol}{sort.value}')
        return paginate(items=users, page=page, page_size=page_size)
