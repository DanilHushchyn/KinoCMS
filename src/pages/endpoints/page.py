from django.http import HttpRequest
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_extra.pagination.decorator import paginate
from ninja_extra.schemas.response import PaginatedResponseSchema

from src.pages.models import Page
from src.pages.schemas.page import (PageInSchema,
                                    PageCardOutSchema,
                                    PageUpdateSchema,
                                    PageOutSchema)
from src.pages.services.page import PageService
from src.core.schemas.base import LangEnum, MessageOutSchema
from ninja_extra.permissions import IsAdminUser
from ninja_extra import http_get, http_post, http_patch, http_delete
from ninja import Header

from src.core.utils import CustomJWTAuth


@api_controller("/page", tags=["pages"])
class CommonController(ControllerBase):
    """
    A controller class for managing page in system.

    This class provides endpoints for
    get, post, update, delete page in the site
    """

    def __init__(self, page_service: PageService):
        """
        Use this method to inject "services" to PageController.

        :param page_service: variable for managing pages
        """
        self.page_service = page_service

    @http_get(
        "/all-cards/",
        # response=PaginatedResponseSchema[PageCardOutSchema],
        response=dict,
        openapi_extra={
            "operationId": "get_all_page_cards",
            "responses": {
                422: {
                    "content": "Error: Unprocessable Entity",
                },
                500: {
                    "content": "Internal server error "
                               "if an unexpected error occurs.",
                },
            },
        },
    )
    # @paginate()
    def get_all_page_cards(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> Page:
        """
        Get all page cards.

        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.page_service.get_all()
        return result

    # @http_post(
    #     "/",
    #     response=MessageOutSchema,
    #     permissions=[IsAdminUser()],
    #     auth=CustomJWTAuth(),
    #     openapi_extra={
    #         "operationId": "create_page",
    #         "responses": {
    #             403: {
    #                 "content": "Error: Forbidden",
    #             },
    #             409: {
    #                 "content": "Error: Conflict",
    #             },
    #             422: {
    #                 "content": "Error: Unprocessable Entity",
    #             },
    #             500: {
    #                 "content": "Internal server error "
    #                            "if an unexpected error occurs.",
    #             },
    #         },
    #     },
    # )
    # def create_page(
    #         self,
    #         request: HttpRequest,
    #         body: PageInSchema,
    #         accept_lang: LangEnum =
    #         Header(alias="Accept-Language",
    #                default="uk"),
    # ) -> MessageOutSchema:
    #     """
    #     Create page.
    #
    #     Please provide:
    #       - **body**  body for creating new page
    #
    #     Returns:
    #       - **200**: Success response with the data.
    #       - **403**: Error: Forbidden. \n
    #         Причини: \n
    #             1) Недійсне значення (не написане великими літерами).
    #                З великих літер повинні починатися (name, content,
    #                seo_title, seo_description) \n
    #       - **409**: Error: Conflict.
    #         Причини: \n
    #             1) Поле name повинно бути унікальним. Ця назва вже зайнята
    #       - **422**: Error: Unprocessable Entity. \n
    #         Причини: \n
    #             1) Максимальни довжина content 20_000 символів \n
    #             2) Максимальни довжина name 60 символів \n
    #             3) Максимальни довжина seo_title 60 символів \n
    #             4) Максимальни довжина seo_description 160 символів \n
    #       - **500**: Internal server error if an unexpected error occurs.
    #     """
    #     result = self.page_service.create(schema=body)
    #     return result
    #
    # @http_patch(
    #     "/{pg_slug}/",
    #     response=MessageOutSchema,
    #     permissions=[IsAdminUser()],
    #     auth=CustomJWTAuth(),
    #     openapi_extra={
    #         "operationId": "update_page",
    #         "responses": {
    #             403: {
    #                 "content": "Error: Forbidden",
    #             },
    #             404: {
    #                 "content": "Error: Not Found",
    #             },
    #             409: {
    #                 "content": "Error: Conflict",
    #             },
    #             422: {
    #                 "content": "Error: Unprocessable Entity",
    #             },
    #             500: {
    #                 "content": "Internal server error "
    #                            "if an unexpected error occurs.",
    #             },
    #         },
    #     },
    # )
    # def update_page(
    #         self,
    #         request: HttpRequest,
    #         pg_slug: str,
    #         body: PageUpdateSchema,
    #         accept_lang: LangEnum =
    #         Header(alias="Accept-Language",
    #                default="uk"),
    # ) -> MessageOutSchema:
    #     """
    #     Update page.
    #
    #     Please provide:
    #       - **body**  body for creating new page
    #
    #     Returns
    #       - **200**: Success response with the data.
    #       - **403**: Error: Forbidden. \n
    #         Причини: \n
    #             1) Недійсне значення (не написане великими літерами).
    #                З великих літер повинні починатися (name, content,
    #                seo_title, seo_description) \n
    #       - **409**: Error: Conflict. \n
    #         Причини: \n
    #             1) Поле name повинно бути унікальним. Ця назва вже зайнята
    #       - **422**: Error: Unprocessable Entity. \n
    #         Причини: \n
    #             1) Максимальни довжина content 20_000 символів \n
    #             2) Максимальни довжина name 60 символів \n
    #             3) Максимальни довжина seo_title 60 символів \n
    #             4) Максимальни довжина seo_description 160 символів \n
    #       - **500**: Internal server error if an unexpected error occurs.
    #     """
    #     result = self.page_service.update(pg_slug=pg_slug, schema=body)
    #     return result
    #
    # @http_get(
    #     "/{pg_slug}/",
    #     response=PageOutSchema,
    #     openapi_extra={
    #         "operationId": "get_page_by_slug",
    #         "responses": {
    #             404: {
    #                 "content": "Error: Not Found",
    #             },
    #             422: {
    #                 "content": "Error: Unprocessable Entity",
    #             },
    #             500: {
    #                 "content": "Internal server error "
    #                            "if an unexpected error occurs.",
    #             },
    #         },
    #     },
    # )
    # def get_page_by_slug(
    #         self,
    #         request: HttpRequest,
    #         pg_slug: str,
    #         accept_lang: LangEnum =
    #         Header(alias="Accept-Language",
    #                default="uk"),
    # ) -> Page:
    #     """
    #     Create page.
    #
    #     Please provide slug:
    #       - **page_slug**  slug of page
    #
    #     Returns:
    #       - **200**: Success response with the data.
    #       - **404**: Error: Forbidden. \n
    #         Причини: \n
    #             1) Не знайдено: немає збігів сторінок
    #                на заданному запиті. \n
    #       - **500**: Internal server error if an unexpected error occurs.
    #     """
    #     result = self.page_service.get_by_slug(pg_slug=pg_slug)
    #     return result
    #
    # @http_delete(
    #     "/{pg_slug}/",
    #     response=MessageOutSchema,
    #     permissions=[IsAdminUser()],
    #     auth=CustomJWTAuth(),
    #     openapi_extra={
    #         "operationId": "delete_page_by_slug",
    #         "responses": {
    #             404: {
    #                 "content": "Error: Not Found",
    #             },
    #             422: {
    #                 "content": "Error: Unprocessable Entity",
    #             },
    #             500: {
    #                 "content": "Internal server error "
    #                            "if an unexpected error occurs.",
    #             },
    #         },
    #     },
    # )
    # def delete_page_by_slug(
    #         self,
    #         request: HttpRequest,
    #         pg_slug: str,
    #         accept_lang: LangEnum =
    #         Header(alias="Accept-Language",
    #                default="uk"),
    # ) -> MessageOutSchema:
    #     """
    #     Delete page by slug.
    #
    #     Please provide:
    #       - **page_slug**  slug of page
    #
    #     Returns:
    #       - **200**: Success response with the data.
    #       - **404**: Error: Forbidden. \n
    #         Причини: \n
    #             1) Не знайдено: немає збігів сторінок
    #                на заданному запиті. \n
    #       - **500**: Internal server error if an unexpected error occurs.
    #     """
    #     result = self.page_service.delete_by_slug(pg_slug=pg_slug)
    #     return result
