# Create your views here.
from django.http import HttpRequest
from ninja_extra.controllers.base import api_controller, ControllerBase

from src.cinemas.models import Cinema
from src.cinemas.schemas.cinema import CinemaInSchema, CinemaCardOutSchema
from src.cinemas.services.cinema import CinemaService
from src.core.schemas.base import LangEnum, MessageOutSchema
from ninja_extra.permissions import IsAdminUser
from ninja_jwt.authentication import JWTAuth
from ninja_extra import http_get, http_post, http_patch, http_delete
from ninja import Header
from django.utils.translation import gettext as _

from src.core.utils import CustomJWTAuth


@api_controller("/cinema", tags=["cinemas"])
class CinemaController(ControllerBase):
    """
    A controller class for managing cinema in system.

    This class provides endpoints for
    get, post, update, delete cinema in the site
    """

    def __init__(self, cinema_service: CinemaService):
        """
        Use this method to inject "services" to CinemaController.

        :param cinema_service: variable for managing cinemas
        """
        self.cinema_service = cinema_service

    @http_post(
        "/",
        response=MessageOutSchema,
        # permissions=[IsAdminUser()],
        # auth=CustomJWTAuth(),
        openapi_extra={
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
          - **404**: Error: Not Found. \n
            Причини: \n
                1) Не знайдено: немає збігів картинок
                   на заданному запиті. \n
                2) Не знайдено: немає збігів галерей
                   на заданному запиті. \n
          - **403**: Error: Forbidden. \n
            Причини: \n
                1) Недійсне значення (не написане великими літерами).
                   З великих літер повинні починатися (name, description,
                   seo_title, seo_description) \n
          - **409**: Error: Conflict.
            Причини: \n
                1) Поле name повинно бути унікальним. Ця назва вже зайнята
          - **422**: Error: Unprocessable Entity. \n
            Причини: \n
                1) Максимальни довжина description 2000 символів \n
                2) Максимальни довжина name 100 символів \n
                3) Максимальни довжина seo_title 60 символів \n
                4) Максимальни довжина seo_description 160 символів \n
          - **500**: Internal server error if an unexpected error occurs.
        """
        self.cinema_service.create(body=body)
        return MessageOutSchema(detail=_('Кінотеатр успішно створений'))

    @http_get(
        "/{cnm_slug}/",
        response=CinemaCardOutSchema,
        openapi_extra={
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
    def get_by_id(
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
    def delete_by_id(
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
