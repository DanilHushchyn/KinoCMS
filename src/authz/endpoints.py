from django.http import HttpRequest
from ninja import Header
from ninja_extra import http_get
from ninja_extra import http_patch
from ninja_extra import http_post
from ninja_extra.controllers.base import ControllerBase
from ninja_extra.controllers.base import api_controller
from ninja_extra.pagination.decorator import paginate
from ninja_extra.permissions.common import AllowAny
from ninja_extra.schemas.response import PaginatedResponseSchema
from ninja_jwt.schema_control import SchemaControl
from ninja_jwt.settings import api_settings

from src.authz.schemas import LoginResponseSchema
from src.authz.schemas import LoginSchema
from src.core.errors import AuthenticationExceptionError
from src.core.errors import InvalidTokenExceptionError
from src.core.errors import NotUniqueFieldExceptionError
from src.core.errors import UnprocessableEntityExceptionError
from src.core.schemas.base import LangEnum
from src.core.schemas.base import MessageOutSchema
from src.core.schemas.base import errors_to_docs
from src.core.utils import CustomJWTAuth
from src.users.models import User
from src.users.schemas import UserOutSchema
from src.users.schemas import UserRegisterSchema
from src.users.schemas import UserUpdateSchema
from src.users.services.user_service import UserService

schema = SchemaControl(api_settings)


@api_controller(
    "/auth",
    permissions=[AllowAny],
    tags=["auth"],
    auth=None,
)
class CustomTokenObtainPairController(ControllerBase):
    """Class controller implements endpoints for
    authorization and authentication
    :param user_service:
    """

    def __init__(self, user_service: UserService):
        """Method for injecting external services and
        initialize reusable data for endpoints
        :param user_service: contains method for
        main purpose this class controller
        """
        self.user_service = user_service

    @http_post(
        "/login",
        response=LoginResponseSchema,
        url_name="token_obtain_pair",
        openapi_extra={
            "operationId": "obtain_token",
            "responses": errors_to_docs(
                {
                    401: [AuthenticationExceptionError(), InvalidTokenExceptionError()],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def obtain_token(
        self,
        request: HttpRequest,
        user_token: LoginSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ):
        """Get user's token by provided credentials.

        Please provide:
          - **Request body**  data with credentials of user

        Returns
        -------
          - **200**: Success response with the data.
          - **401**: Error: Unauthorized.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.

        """
        user_token.check_user_authentication_rule()
        return user_token.to_response_schema()

    @http_post(
        "/blacklist",
        response={200: schema.blacklist_schema.get_response_schema()},
        url_name="token_blacklist",
        openapi_extra={
            "operationId": "blacklist_token",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def blacklist_token(
        self,
        request: HttpRequest,
        refresh: schema.blacklist_schema,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ):
        """Makes refresh token blacklisted;

        Please provide:
          - **Request body**  data with credentials of user

        Returns
        -------
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.

        """
        return refresh.to_response_schema()

    @http_post(
        "/refresh",
        response=schema.obtain_pair_refresh_schema.get_response_schema(),
        url_name="token_refresh",
        openapi_extra={
            "operationId": "refresh_token",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def refresh_token(
        self,
        request: HttpRequest,
        refresh_token: schema.obtain_pair_refresh_schema,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ):
        """Get user's new access token by provided refresh token.

        Please provide:
          - **Request body**  provide here refresh token

        Returns
        -------
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
            "operationId": "register",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    409: [NotUniqueFieldExceptionError(field="email")],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def register(
        self,
        request: HttpRequest,
        user_body: UserRegisterSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> MessageOutSchema:
        """Register new user.

        Please provide:
          - **Request body**  data for registration new user

        Returns
        -------
          - **200**: Success response with the data.
          - **409**: Error: Conflict. \n
            Причини: \n
                1) Ця електронна адреса вже використовується
          - **422**: Error: Unprocessable Entity.
            Причини: \n
                1) Паролі не співпадають \n
                2) Пароль повинен бути: \n
                   * Принаймні одна велика літера \n
                   * Принаймні одна мала літера \n
                   * Принаймні одна цифра \n
                   * Принаймні один спеціальний символ із набору ?!@%^&- \n
                   * Мінімальна довжина 8 символів \n
                3) Введено некоректний номер телефону \n
                4) Ім'я та прізвище повинно починатися з великої літери \n
                   (наступні маленькі), доступна кирилиця,
                   доступні спецсимволи('-) \n
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.user_service.register(user_body=user_body)
        return result

    @http_get(
        "/cities/choices/",
        response=PaginatedResponseSchema[list],
        openapi_extra={
            "operationId": "get_cities",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    @paginate()
    def get_cities(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> list:
        """Endpoint gets cities for user to choose.

        Returns
        -------
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.user_service.get_cities()
        return result

    @http_get(
        "/my-profile/",
        response=UserOutSchema,
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "get_my_profile",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_my_profile(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> User:
        """Get user's personal data by token.

        Please provide:
          - **Request body**  data for registration new user

        Returns
        -------
          - **200**: Success response with the data.
          - **401**: Error: Unauthorized. \n
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.

        """
        return request.user

    @http_patch(
        "/my-profile/",
        response=UserOutSchema,
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "update_my_profile",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    409: [NotUniqueFieldExceptionError(field="email")],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def update_my_profile(
        self,
        request: HttpRequest,
        user_body: UserUpdateSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> User:
        """Get user's personal data by token.

        Please provide:
          - **Request body**  data for registration new user

        Returns
        -------
          - **200**: Success response with the data.
          - **401**: Error: Unauthorized. \n
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.user_service.update_by_id(request.user.id, user_body)
        return result
