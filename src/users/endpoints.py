from typing import Optional

from django.core.exceptions import ValidationError
from django.http import HttpRequest
from ninja import Header
from ninja_extra.controllers.base import api_controller, ControllerBase

from ninja.errors import HttpError
from django.utils.translation import gettext as _
from ninja_extra.permissions import IsAdminUser
from ninja_jwt.authentication import JWTAuth

from src.core.schemas import LangEnum, MessageOutSchema
from src.users.models import User
from src.users.schemas import (UserRegisterSchema, UserUpdateSchema,
                               UserOutSchema, UsersAllSchema)
from src.users.services.user_service import UserService
from ninja_extra import http_delete, http_get, http_patch, http_post


@api_controller("/users", tags=["users"])
class UsersKinoController(ControllerBase):
    """
    A controller class for managing user's personal data.

    This class provides endpoints for
    get, post, update, create users in the site
    """

    def __init__(self, user_service: UserService):
        """
        Use this method to inject "services" to UsersController.

        :param user_service: variable for managing access control system
        """
        self.user_service = user_service

    @http_post(
        "/register/",
        response=MessageOutSchema,
        openapi_extra={
            "responses": {
                409: {
                    "description": "Error: Conflict",
                },
                403: {
                    "description": "Error: Forbidden",
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error "
                                   "if an unexpected error occurs.",
                },
            },
        },
    )
    def register(
            self,
            request: HttpRequest,
            user_body: UserRegisterSchema,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Register new user.

        Please provide:
          - **Request body**  data for registration new user

        Returns:
          - **200**: Success response with the data.
          - **403**: Error: Forbidden. \n
              Причини:
              1) Паролі не співпадають
              2) Пароль повинен бути:
                 * Принаймні одна велика літера
                 * Принаймні одна мала літера
                 * Принаймні одна цифра
                 * Принаймні один спеціальний символ із набору ?!@%^&-
                 * Мінімальна довжина 8 символів
              3) Введено некоректний номер телефону
              4) Ім'я та прізвище повинно починатися з великої літери"
                 (наступні маленькі), доступна кирилиця,
                 доступні спецсимволи('-)
          - **409**: Error: Conflict. \n
              Причини:
              1) Ця електронна адреса вже використовується
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.user_service.register(user_body=user_body)
        return result


@api_controller("/users", tags=["users"])
class UsersAdminController(ControllerBase):
    """
    A controller class for managing user's personal data.

    This class provides endpoints for
    get, post, update, create users in the site
    """

    def __init__(self, user_service: UserService):
        """
        Use this method to inject "services" to UsersController.

        :param user_service: variable for managing access control system
        """
        self.user_service = user_service

    @http_patch(
        "/detail/{user_id}/",
        auth=JWTAuth(),
        permissions=[IsAdminUser()],
        response=UserOutSchema,
        openapi_extra={
            "responses": {
                403: {
                    "description": "Error: Forbidden",
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error "
                                   "if an unexpected error occurs.",
                },
            },
        },
    )
    def update_by_id(
            self,
            request: HttpRequest,
            user_id: int,
            user_body: UserUpdateSchema,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> User:
        """
        Update user by id.

        Please provide:
          - **Request body**  data for updating user

        Returns:
          - **200**: Success response with the data.
          - **403**: Error: Forbidden. \n
              Причини:
              1) Введено некоректний номер телефону
              2) Ім'я та прізвище повинно починатися з великої літери
                 (наступні маленькі), доступна кирилиця,
                 доступні спецсимволи('-)
          - **404**: Error: Conflict. \n
              Причини:
              1) Не знайдено: немає збігів користувачів
              на заданному запиті.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        user = self.user_service.update_by_id(user_id=user_id,
                                              user_body=user_body)
        return user

    @http_get(
        "/detail/{user_id}/",
        response=UserOutSchema,
        auth=JWTAuth(),

        permissions=[IsAdminUser()],
        openapi_extra={
            "responses": {
                404: {
                    "description": "Error: Conflict",
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_by_id(
            self,
            request: HttpRequest,
            user_id: int,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> User:
        """
        Register new user.

        Please provide:
          - **Request body**  data for registration new user

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Conflict. \n
              Причини:
              1) Не знайдено: немає збігів користувачів
              на заданному запиті.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.user_service.get_by_id(user_id=user_id)
        return result

    @http_delete(
        "/detail/{user_id}/",
        auth=JWTAuth(),
        permissions=[IsAdminUser()],
        response=MessageOutSchema,
        openapi_extra={
            "responses": {
                404: {
                    "description": "Error: Conflict",
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def delete_by_id(
            self,
            request: HttpRequest,
            user_id: int,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Register new user.

        Please provide:
          - **Request body**  data for registration new user

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Conflict. \n
              Причини:
              1) Не знайдено: немає збігів користувачів
              на заданному запиті.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.user_service.delete_by_id(user_id=user_id)
        return result

    @http_get(
        "/all/",
        response=UsersAllSchema,
        auth=JWTAuth(),
        permissions=[IsAdminUser()],
        openapi_extra={
            "responses": {
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error if" " an unexpected error occurs.",
                },
            },
        },
    )
    def get_all(
            self,
            request: HttpRequest,
            page: int,
            page_size: int,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> dict:
        """
        Endpoint gets all users.

        Makes pagination of records.

        Please provide:
         - **page**  number of page we want to get
         - **page_size**  length of records per page

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.user_service.get_all(page, page_size)
        return result

    @http_get(
        "/search/{search_line}/",
        response=UsersAllSchema,
        auth=JWTAuth(),
        permissions=[IsAdminUser()],
        openapi_extra={
            "responses": {
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error if an unexpected error occurs.",
                },
            },
        },
    )
    def search(
            self,
            request: HttpRequest,
            search_line: str,
            page: int,
            page_size: int,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> dict:
        """
        Endpoint gets all users.

        Makes pagination of records.

        Please provide:
         - **page**  number of page we want to get
         - **page_size**  length of records per page

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.user_service.search(search_line, page, page_size)
        return result

