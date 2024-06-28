from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Header
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_extra.pagination.decorator import paginate
from ninja_extra.permissions import IsAdminUser
from ninja_extra.schemas.response import PaginatedResponseSchema

from src.authz.errors import EmailAlreadyExistsExceptionError
from src.core.errors import InvalidTokenExceptionError, UnprocessableEntityExceptionError
from src.core.schemas.base import (LangEnum, MessageOutSchema,
                                   DirectionEnum, errors_to_docs)
from src.core.utils import CustomJWTAuth
from src.users.models import User
from src.users.schemas import (UserUpdateSchema,
                               UserOutSchema,
                               UserFieldsEnum)
from src.users.services.user_service import UserService
from ninja_extra import http_delete, http_get, http_patch


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
        auth=CustomJWTAuth(),
        permissions=[IsAdminUser()],
        response=UserOutSchema,
        openapi_extra={
            "operationId": "update_user_by_id",
            "responses": errors_to_docs({
                401: [
                    InvalidTokenExceptionError()
                ],
                404: [
                    InvalidTokenExceptionError()
                ],
                409: [
                    EmailAlreadyExistsExceptionError()
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def update_user_by_id(
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
          - **404**: Error: Conflict. \n
            Причини: \n
                1) Не знайдено: немає збігів користувачів
                   на заданному запиті.
          - **422**: Error: Unprocessable Entity.
            Причини: \n
                1) Введено некоректний номер телефону \n
                2) Ім'я та прізвище повинно починатися з великої літери
                   (наступні маленькі), доступна кирилиця,
                   доступні спецсимволи('-)
          - **500**: Internal server error if an unexpected error occurs.
        """
        user = self.user_service.update_by_id(user_id=user_id,
                                              user_body=user_body)
        return user

    @http_get(
        "/detail/{user_id}/",
        response=UserOutSchema,
        auth=CustomJWTAuth(),
        permissions=[IsAdminUser()],
        openapi_extra={
            "operationId": "get_user_by_id",
            "responses": errors_to_docs({
                401: [
                    InvalidTokenExceptionError()
                ],
                404: [
                    InvalidTokenExceptionError()
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def get_user_by_id(
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
            Причини: \n
                1) Не знайдено: немає збігів користувачів
                   на заданному запиті.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.user_service.get_by_id(user_id=user_id)
        return result

    @http_delete(
        "/detail/{user_id}/",
        auth=CustomJWTAuth(),
        permissions=[IsAdminUser()],
        response=MessageOutSchema,
        openapi_extra={
            "operationId": "delete_user_by_id",
            "responses": errors_to_docs({
                401: [
                    InvalidTokenExceptionError()
                ],
                404: [
                    InvalidTokenExceptionError()
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def delete_user_by_id(
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
            Причини: \n
                1) Не знайдено: немає збігів користувачів
                   на заданному запиті.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.user_service.delete_by_id(user_id=user_id)
        return result

    @http_get(
        "/datable/",
        response=PaginatedResponseSchema[UserOutSchema],
        auth=CustomJWTAuth(),
        permissions=[IsAdminUser()],
        openapi_extra={
            "operationId": "users_datatable",
            "responses": errors_to_docs({
                401: [
                    InvalidTokenExceptionError()
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    @paginate()
    def users_datatable(
            self,
            request: HttpRequest,
            search_line: str = None,
            sort: UserFieldsEnum = None,
            direction: DirectionEnum = DirectionEnum.Descending,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> QuerySet:
        """
        Endpoint gets all users.

        Makes pagination, search and sorting of records.

        Please provide:
         - **page**  number of page we want to get
         - **page_size**  length of records per page
         - **search_line**  helps to find rows which contains search line
         - **sort**  define by which field sort rows
         - **direction**  determines in which direction to sort

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.user_service.search(search_line, sort, direction)
        return result
