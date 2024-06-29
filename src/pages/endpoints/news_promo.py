from django.db.models import QuerySet
from django.http import HttpRequest
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_extra.pagination.decorator import paginate
from ninja_extra.schemas.response import PaginatedResponseSchema

from src.core.errors import UnprocessableEntityExceptionError, InvalidTokenExceptionError, NotFoundExceptionError, \
    NotUniqueFieldExceptionError
from src.core.models import Image
from src.pages.models import NewsPromo
from src.pages.schemas.news_promo import (NewsPromoInSchema,
                                          NewsPromoCardOutSchema,
                                          NewsPromoUpdateSchema,
                                          NewsPromoOutSchema,
                                          NewsPromoClientOutSchema)
from src.pages.services.news_promo import NewsPromoService
from src.core.schemas.base import LangEnum, MessageOutSchema, errors_to_docs
from ninja_extra.permissions import IsAdminUser
from ninja_extra import http_get, http_post, http_patch, http_delete
from ninja import Header

from src.core.utils import CustomJWTAuth


@api_controller("/news_promo", tags=["news_promos"])
class NewsPromoController(ControllerBase):
    """
    A controller class for managing news_promo in system.

    This class provides endpoints for
    get, post, update, delete news_promo in the site
    """

    def __init__(self, news_promo_service: NewsPromoService):
        """
        Use this method to inject "services" to NewsPromoController.

        :param news_promo_service: variable for managing news_promos
        """
        self.news_promo_service = news_promo_service

    @http_get(
        "/all-cards/",
        response=PaginatedResponseSchema[NewsPromoCardOutSchema],
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "get_all_news_promo_cards",
            "responses": errors_to_docs({
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    @paginate()
    def get_all_news_promo_cards(
            self,
            request: HttpRequest,
            promo: bool,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> NewsPromo:
        """
        Get all news_promo cards.

        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.news_promo_service.get_all(promo)
        return result

    @http_post(
        "/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "create_news_promo",
            "responses": errors_to_docs({
                401: [
                    InvalidTokenExceptionError()
                ],
                404: [
                    NotFoundExceptionError(cls_model=NewsPromo)
                ],
                409: [
                    NotUniqueFieldExceptionError(field='name')
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def create_news_promo(
            self,
            request: HttpRequest,
            body: NewsPromoInSchema,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Create news_promo.

        Please provide:
          - **body**  body for creating new news_promo

        Returns:
          - **200**: Success response with the data.
          - **409**: Error: Conflict.
            Причини: \n
                1) Поле name повинно бути унікальним. Ця назва вже зайнята
          - **422**: Error: Unprocessable Entity. \n
            Причини: \n
                1) Максимальни довжина description 20_000 символів \n
                2) Максимальни довжина name 60 символів \n
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
                 a) required image if filename is specified.
                    Format base64(svg,png,jpg,jpeg,webp) \n
                 b) filename is required if image is specified.
                    Example: *filename.png* \n
                 c) optional alt. If you don't specify it,
                    I'll take the value from filename \n
         - Create:
             1. Do not specify the id field \n
             3. Be sure to specify the image field \n
                 a) required image if filename is specified.
                    Format base64(svg,png,jpg,jpeg,webp) \n
                 b) filename is required if image is specified.
                    Example: *filename.png* \n
                 c) optional alt. If you don't specify it,
                    I'll take the value from filename \n
             4. Be sure to specify the field delete=false \n
        """
        result = self.news_promo_service.create(schema=body,
                                                request=request)
        return result

    @http_patch(
        "/{np_slug}/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "update_news_promo",
            "responses": errors_to_docs({
                401: [
                    InvalidTokenExceptionError()
                ],
                404: [
                    NotFoundExceptionError(cls_model=NewsPromo),
                    NotFoundExceptionError(cls_model=Image)
                ],
                409: [
                    NotUniqueFieldExceptionError(field='name')
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def update_news_promo(
            self,
            request: HttpRequest,
            np_slug: str,
            body: NewsPromoUpdateSchema,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Update news_promo.

        Please provide:
          - **body**  body for creating new news_promo

        Returns
          - **200**: Success response with the data.
          - **409**: Error: Conflict. \n
            Причини: \n
                1) Поле name повинно бути унікальним. Ця назва вже зайнята
          - **422**: Error: Unprocessable Entity. \n
            Причини: \n
                1) Максимальни довжина description 20_000 символів \n
                2) Максимальни довжина name 60 символів \n
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
        result = self.news_promo_service.update(request=request,
                                                np_slug=np_slug,
                                                schema=body)
        return result

    @http_get(
        "/{np_slug}/",
        response=NewsPromoOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "get_news_promo_by_slug",
            "responses": errors_to_docs({
                401: [
                    InvalidTokenExceptionError()
                ],
                404: [
                    NotFoundExceptionError(cls_model=NewsPromo)
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def get_news_promo_by_slug(
            self,
            request: HttpRequest,
            np_slug: str,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> NewsPromo:
        """
        Get news or promo by slug.

        Please provide slug:
          - **news_promo_slug**  slug of news or promo

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Forbidden. \n
            Причини: \n
                1) Не знайдено: немає збігів новин чи акцій
                   на заданному запиті. \n
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.news_promo_service.get_by_slug(np_slug=np_slug)
        return result

    @http_delete(
        "/{np_slug}/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "delete_news_promo_by_slug",
            "responses": errors_to_docs({
                401: [
                    InvalidTokenExceptionError()
                ],
                404: [
                    NotFoundExceptionError(cls_model=NewsPromo)
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def delete_news_promo_by_slug(
            self,
            request: HttpRequest,
            np_slug: str,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Delete news_promo by slug.

        Please provide:
          - **news_promo_slug**  slug of news_promo

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Forbidden. \n
            Причини: \n
                1) Не знайдено: немає збігів новин чи акцій
                   на заданному запиті. \n
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.news_promo_service.delete_by_slug(np_slug=np_slug)
        return result


@api_controller("/news_promo", tags=["news_promos"])
class NewsPromoClientController(ControllerBase):
    """
    A controller class for managing news_promo in system.

    This class provides endpoints for
    get, post, update, delete news_promo in the site
    """

    def __init__(self, news_promo_service: NewsPromoService):
        """
        Use this method to inject "services" to NewsPromoController.

        :param news_promo_service: variable for managing news_promos
        """
        self.news_promo_service = news_promo_service

    @http_get(
        "/all-cards/",
        response=PaginatedResponseSchema[NewsPromoCardOutSchema],
        openapi_extra={
            "operationId": "get_all_news_promo_cards",
            "responses": errors_to_docs({
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    @paginate()
    def get_all_news_promo_cards(
            self,
            request: HttpRequest,
            promo: bool,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> QuerySet[NewsPromo]:
        """
        Get all news_promo cards for client site.

        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.news_promo_service.get_all_active(promo)
        return result

    @http_get(
        "/{np_slug}/",
        response=NewsPromoClientOutSchema,
        openapi_extra={
            "operationId": "get_news_promo_by_slug",
            "responses": errors_to_docs({
                404: [
                    NotFoundExceptionError(cls_model=NewsPromo)
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def get_news_promo_by_slug(
            self,
            request: HttpRequest,
            np_slug: str,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> NewsPromo:
        """
        Get news or promo by slug.

        Please provide slug:
          - **news_promo_slug**  slug of news or promo

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Forbidden. \n
            Причини: \n
                1) Не знайдено: немає збігів новин чи акцій
                   на заданному запиті. \n
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = (self.news_promo_service
                  .get_active_by_slug(np_slug=np_slug))
        return result
