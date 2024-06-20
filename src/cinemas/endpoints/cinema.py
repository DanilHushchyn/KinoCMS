from django.http import HttpRequest
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_extra.pagination.decorator import paginate
from ninja_extra.schemas.response import PaginatedResponseSchema
from src.cinemas.models import Cinema
from src.cinemas.schemas.cinema import (CinemaInSchema,
                                        CinemaCardOutSchema,
                                        CinemaUpdateSchema,
                                        CinemaOutSchema, CinemaContactOutSchema)
from src.cinemas.services.cinema import CinemaService
from src.core.schemas.base import LangEnum, MessageOutSchema
from ninja_extra.permissions import IsAdminUser
from ninja_extra import (http_get, http_post, http_patch,
                         http_delete,
                         route)
from ninja import Header
from django.utils.translation import gettext as _

from src.core.utils import CustomJWTAuth


@api_controller("/cinema", tags=["cinemas"])
class CinemaController(ControllerBase):
    """
    A controller class for managing cinema in admin site.

    This class provides endpoints for
    get, post, update, delete cinema in the site
    """

    def __init__(self, cinema_service: CinemaService):
        """
        Use this method to inject "services" to CinemaController.

        :param cinema_service: variable for managing cinemas
        """
        self.cinema_service = cinema_service

    @http_get(
        "/all-cards/",
        response=PaginatedResponseSchema[CinemaCardOutSchema],
        openapi_extra={
            "operationId": "get_all_cinema_cards",
            "responses": {
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
    @paginate()
    def get_all_cinema_cards(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> Cinema:
        """
        Get all cinema cards.

        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.cinema_service.get_all()
        return result

    @http_post(
        "/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "create_cinema",
            "responses": {
                403: {
                    "description": "Error: Forbidden",
                },
                409: {
                    "description": "Error: Conflict",
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
    def create_cinema(
            self,
            request: HttpRequest,
            body: CinemaInSchema,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Create cinema.

        Please provide:
          - **body**  body for creating new cinema

        Returns:
          - **200**: Success response with the data.
          - **403**: Error: Forbidden. \n
            Причини: \n
                1) Недійсне значення (не написане великими літерами).
                   З великих літер повинні починатися (name, description,
                   seo_title, seo_description) \n
                2) Введено некоректний номер телефону \n
          - **409**: Error: Conflict.
            Причини: \n
                1) Поле name повинно бути унікальним. Ця назва вже зайнята
          - **422**: Error: Unprocessable Entity. \n
            Причини: \n
                1) Максимальни довжина description 20_000 символів \n
                2) Максимальни довжина name 100 символів \n
                3) Максимальни довжина seo_title 60 символів \n
                4) Максимальни довжина seo_description 160 символів \n
          - **500**: Internal server error if an unexpected error occurs.

        Operations with gallery items:
         - Delete \n
             1. Be sure to specify the id field \n
             2. Be sure to specify the field delete=true \n
         - Update \n
             1. Be sure to specify the id field \n
             2. Be sure to specify the field delete=false \n
             3. Be sure to specify the image field \n
                 a) required image if filename is specified. Format base64(svg,png,jpg,jpeg,webp) \n
                 b) filename is required if image is specified. Example: *filename.png* \n
                 c) optional alt. If you don't specify it, I'll take the value from filename \n
         - Create:
             1. Do not specify the id field \n
             3. Be sure to specify the image field \n
                 a) required image if filename is specified. Format base64(svg,png,jpg,jpeg,webp) \n
                 b) filename is required if image is specified. Example: *filename.png* \n
                 c) optional alt. If you don't specify it, I'll take the value from filename \n
             4. Be sure to specify the field delete=false \n
        """
        result = self.cinema_service.create(request=request, schema=body)
        return result

    @http_patch(
        "/{cnm_slug}/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "update_cinema",
            "responses": {
                403: {
                    "description": "Error: Forbidden",
                },
                404: {
                    "description": "Error: Not Found",
                },
                409: {
                    "description": "Error: Conflict",
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
    def update_cinema(
            self,
            request: HttpRequest,
            cnm_slug: str,
            body: CinemaUpdateSchema,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Update cinema.

        Please provide:
          - **body**  body for creating new cinema

        Returns
          - **200**: Success response with the data.
          - **403**: Error: Forbidden. \n
            Причини: \n
                1) Недійсне значення (не написане великими літерами).
                   З великих літер повинні починатися (name, description,
                   seo_title, seo_description) \n
                2) Введено некоректний номер телефону \n
          - **409**: Error: Conflict. \n
            Причини: \n
                1) Поле name повинно бути унікальним. Ця назва вже зайнята
          - **422**: Error: Unprocessable Entity. \n
            Причини: \n
                1) Максимальни довжина description 20_000 символів \n
                2) Максимальни довжина name 100 символів \n
                3) Максимальни довжина seo_title 60 символів \n
                4) Максимальни довжина seo_description 160 символів \n
          - **500**: Internal server error if an unexpected error occurs.


        Operations with gallery items:
         - Delete \n
             1. Be sure to specify the id field \n
             2. Be sure to specify the field delete=true \n
         - Update \n
             1. Be sure to specify the id field \n
             2. Be sure to specify the field delete=false \n
             3. Be sure to specify the image field \n
                 a) required image if filename is specified. Format base64(svg,png,jpg,jpeg,webp) \n
                 b) filename is required if image is specified. Example: *filename.png* \n
                 c) optional alt. If you don't specify it, I'll take the value from filename \n
         - Create:
             1. Do not specify the id field \n
             3. Be sure to specify the image field \n
                 a) required image if filename is specified. Format base64(svg,png,jpg,jpeg,webp) \n
                 b) filename is required if image is specified. Example: *filename.png* \n
                 c) optional alt. If you don't specify it, I'll take the value from filename \n
             4. Be sure to specify the field delete=false \n
        """
        self.cinema_service.update(request=request,
                                   cnm_slug=cnm_slug,
                                   schema=body)
        return MessageOutSchema(detail=_('Кінотеатр успішно оновлений'))

    @http_get(
        "/{cnm_slug}/",
        response=CinemaOutSchema,
        openapi_extra={
            "operationId": "get_cinema_by_slug",
            "responses": {
                404: {
                    "description": "Error: Not Found",
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
    def get_cinema_by_slug(
            self,
            request: HttpRequest,
            cnm_slug: str,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> Cinema:
        """
        Create cinema.

        Please provide:
          - **cinema_id**  id of cinema

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Forbidden. \n
            Причини: \n
                1) Не знайдено: немає збігів кінотеатрів
                   на заданному запиті. \n
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.cinema_service.get_by_slug(cnm_slug=cnm_slug)
        return result

    @http_delete(
        "/{cnm_slug}/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "delete_cinema_by_slug",
            "responses": {
                404: {
                    "description": "Error: Not Found",
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
    def delete_cinema_by_slug(
            self,
            request: HttpRequest,
            cnm_slug: str,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Delete cinema by id.

        Please provide:
          - **cinema_id**  id of cinema

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Forbidden. \n
            Причини: \n
                1) Не знайдено: немає збігів кінотеатрів
                   на заданному запиті. \n
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.cinema_service.delete_by_slug(cnm_slug=cnm_slug)
        return result


@api_controller("/cinema", tags=["cinemas"])
class CinemaClientController(ControllerBase):
    """
    A controller class for managing cinema in client site.

    This class provides endpoints for
    get, cinema in the site
    """

    def __init__(self, cinema_service: CinemaService):
        """
        Use this method to inject "services" to CinemaController.

        :param cinema_service: variable for managing cinemas
        """
        self.cinema_service = cinema_service
    get_all_cinema_cards = CinemaController.get_all_cinema_cards

    @http_get(
        "/all-contacts/",
        response=PaginatedResponseSchema[CinemaContactOutSchema],
        openapi_extra={
            "operationId": "get_all_cinema_contacts",
            "responses": {
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
    @paginate()
    def get_all_cinema_contacts(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> Cinema:
        """
        Get all cinema cards.

        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.cinema_service.get_all()
        return result

    get_cinema_by_slug = CinemaController.get_cinema_by_slug

