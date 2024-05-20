from typing import Tuple, List

from django.http import HttpRequest
from ninja_extra import http_post, http_get, http_patch
from ninja_extra.controllers.base import ControllerBase, api_controller
from ninja_extra.permissions.common import AllowAny
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.schema_control import SchemaControl
from ninja_jwt.settings import api_settings
from src.authz.schemas import LoginSchema, LoginResponseSchema
from src.users.models import User
from src.users.schemas import UserOutSchema, UserUpdateSchema, UserRegisterSchema
from src.users.services.user_service import UserService
from src.core.schemas import LangEnum, MessageOutSchema
from ninja import Header

schema = SchemaControl(api_settings)


@api_controller(
    "/auth",
    permissions=[AllowAny],
    tags=["auth"],
    auth=None,
)
class CustomTokenObtainPairController(ControllerBase):

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @http_post(
        "/login",
        response=LoginResponseSchema,
        url_name="token_obtain_pair",
        openapi_extra={
            "responses": {
                401: {
                    "description": "Error: Unauthorized",
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
    def obtain_token(self, request: HttpRequest,
                     user_token: LoginSchema,
                     accept_lang: LangEnum =
                     Header(alias="Accept-Language",
                            default="uk"),
                     ):
        """
        Get user's token by provided credentials.

        Please provide:
          - **Request body**  data with credentials of user

        Returns:
          - **200**: Success response with the data.
          - **401**: Error: Unauthorized.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        user_token.check_user_authentication_rule()
        return user_token.to_response_schema()

    @http_post(
        "/refresh",
        response=schema.obtain_pair_refresh_schema.get_response_schema(),
        url_name="token_refresh",
        openapi_extra={
            "responses": {
                401: {
                    "description": "Error: Unauthorized",
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
    def refresh_token(
            self,
            request: HttpRequest,
            refresh_token: schema.obtain_pair_refresh_schema,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),

    ):
        """
        Get user's new access token by provided refresh token.

        Please provide:
          - **Request body**  provide here refresh token

        Returns:
          - **200**: Success response with the data.
          - **401**: Error: Unauthorized.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        return refresh_token.to_response_schema()

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

    @http_get(
        "/cities/choices/",
        response=List,
        # auth=JWTAuth(),
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
    def get_cities(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> List:
        """
        Endpoint gets cities for user to choose.
        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.user_service.get_cities()
        return result

    @http_get(
        "/my-profile/",
        response=UserOutSchema,
        auth=JWTAuth(),
        openapi_extra={
            "responses": {
                401: {
                    "description": "Error: Unauthorized",
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error if an unexpected error occurs.",
                },
            },
        },
    )
    def get_my_profile(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> User:
        """
        Get user's personal data by token.

        Please provide:
          - **Request body**  data for registration new user

        Returns:
          - **200**: Success response with the data.
          - **401**: Error: Unauthorized. \n
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        # result = self.user_service.get_by_id(request.user.id)
        return request.user

    @http_patch(
        "/my-profile/",
        response=UserOutSchema,
        auth=JWTAuth(),
        openapi_extra={
            "responses": {
                401: {
                    "description": "Error: Unauthorized",
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error if an unexpected error occurs.",
                },
            },
        },
    )
    def update_my_profile(
            self,
            request: HttpRequest,
            user_body: UserUpdateSchema,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> User:
        """
        Get user's personal data by token.

        Please provide:
          - **Request body**  data for registration new user

        Returns:
          - **200**: Success response with the data.
          - **401**: Error: Unauthorized. \n
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.user_service.update_by_id(request.user.id,
                                                user_body)
        return result




