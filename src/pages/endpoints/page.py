"""Page essence endpoints"""

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Header
from ninja_extra import http_delete
from ninja_extra import http_get
from ninja_extra import http_patch
from ninja_extra import http_post
from ninja_extra.controllers.base import ControllerBase
from ninja_extra.controllers.base import api_controller
from ninja_extra.pagination.decorator import paginate
from ninja_extra.permissions import IsAdminUser
from ninja_extra.schemas.response import PaginatedResponseSchema

from src.core.errors import InvalidTokenExceptionError
from src.core.errors import NotFoundExceptionError
from src.core.errors import NotUniqueFieldExceptionError
from src.core.errors import UnprocessableEntityExceptionError
from src.core.models import Image
from src.core.schemas.base import LangEnum
from src.core.schemas.base import MessageOutSchema
from src.core.schemas.base import errors_to_docs
from src.core.utils import CustomJWTAuth
from src.pages.errors import PageUnableToDeleteExceptionError
from src.pages.models import Page
from src.pages.schemas.page import PageCardClientOutSchema
from src.pages.schemas.page import PageCardOutSchema
from src.pages.schemas.page import PageClientOutSchema
from src.pages.schemas.page import PageInSchema
from src.pages.schemas.page import PageOutSchema
from src.pages.schemas.page import PageUpdateSchema
from src.pages.services.page import PageService


@api_controller("/page", tags=["pages"])
class PageController(ControllerBase):
    """A controller class for managing pages in system.

    This class provides endpoints for
    get, post, update, delete page in the site
    """

    def __init__(self, page_service: PageService):
        """Use this method to inject "services" to PageController.

        :param page_service: variable for managing pages
        """
        self.page_service = page_service

    @http_get(
        "/all-cards/",
        response=PaginatedResponseSchema[PageCardOutSchema],
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "get_all_page_cards",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    @paginate()
    def get_all_page_cards(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> QuerySet[Page]:
        """Get all page cards.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.page_service.get_all()
        return result

    @http_post(
        "/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "create_page",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    409: [NotUniqueFieldExceptionError(field="name")],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def create_page(
        self,
        request: HttpRequest,
        body: PageInSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> MessageOutSchema:
        """Create page.

        Please provide:
          - **body**  body for creating new page

        Returns
        -------
          - **200**: Success response with the data.
          - **409**: Error: Conflict.
            Причини: \n
                1) Поле name повинно бути унікальним. Ця назва вже зайнята
          - **422**: Error: Unprocessable Entity. \n
            Причини: \n
                1) Максимальни довжина name 60 символів \n
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
        result = self.page_service.create(request=request, schema=body)
        return result

    @http_patch(
        "/{pg_slug}/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "update_page",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    404: [
                        NotFoundExceptionError(cls_model=Page),
                        NotFoundExceptionError(cls_model=Image),
                    ],
                    409: [NotUniqueFieldExceptionError(field="name")],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def update_page(
        self,
        request: HttpRequest,
        pg_slug: str,
        body: PageUpdateSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> MessageOutSchema:
        """Update page.

        Please provide:
          - **body**  body for creating new page

        Returns
        -------
          - **200**: Success response with the data.
          - **409**: Error: Conflict. \n
            Причини: \n
                1) Поле name повинно бути унікальним. Ця назва вже зайнята
          - **422**: Error: Unprocessable Entity. \n
            Причини: \n
                1) Максимальни довжина name 60 символів \n
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
        result = self.page_service.update(request=request, pg_slug=pg_slug, schema=body)
        return result

    @http_get(
        "/{pg_slug}/",
        response={
            200: PageOutSchema,
        },
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "get_page_by_slug",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    404: [NotFoundExceptionError(cls_model=Page)],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_page_by_slug(
        self,
        request: HttpRequest,
        pg_slug: str,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> Page:
        """Create page.

        Please provide:
          - **pg_slug**  slug of page

        Returns
        -------
          - **200**: Success response with the data.
          - **404**: Error: Forbidden. \n
            Причини: \n
                1) Не знайдено: немає збігів сторінок
                   на заданному запиті. \n
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.page_service.get_by_slug(pg_slug=pg_slug)
        return result

    @http_delete(
        "/{pg_slug}/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "delete_page_by_slug",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    404: [NotFoundExceptionError(cls_model=Page)],
                    406: [PageUnableToDeleteExceptionError()],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def delete_page_by_slug(
        self,
        request: HttpRequest,
        pg_slug: str,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> MessageOutSchema:
        """Delete page by slug.

        Please provide:
          - **pg_slug**  slug of page

        Returns
        -------
          - **200**: Success response with the data. \n
          - **406**: Error: Conflict. \n
            Причини: \n
                1) Цю сторінку заборонено видаляти. \n
          - **404**: Error: Forbidden. \n
            Причини: \n
                1) Не знайдено: немає збігів сторінок
                   на заданному запиті. \n
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.page_service.delete_by_slug(pg_slug=pg_slug)
        return result


@api_controller("/page", tags=["pages"])
class PageClientController(ControllerBase):
    """A controller class for managing pages in system.

    This class provides endpoints for
    get, post, update, delete page in the site
    """

    def __init__(self, page_service: PageService):
        """Use this method to inject "services" to PageController.

        :param page_service: variable for managing pages
        """
        self.page_service = page_service

    @http_get(
        "/all/",
        response=PaginatedResponseSchema[PageCardClientOutSchema],
        openapi_extra={
            "operationId": "get_all_page_cards",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    @paginate()
    def get_all_page_cards(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> QuerySet[Page]:
        """Get all page cards.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.page_service.get_all_active()
        return result

    @http_get(
        "/{pg_slug}/",
        response=PageClientOutSchema,
        openapi_extra={
            "operationId": "get_page_by_slug",
            "responses": errors_to_docs(
                {
                    404: [NotFoundExceptionError(cls_model=Page)],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_page_by_slug(
        self,
        request: HttpRequest,
        pg_slug: str,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> Page:
        """Create page.

        Please provide:
          - **pg_slug**  slug of page

        Returns
        -------
          - **200**: Success response with the data.
          - **404**: Error: Forbidden. \n
            Причини: \n
                1) Не знайдено: немає збігів сторінок
                   на заданному запиті. \n
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.page_service.get_active_by_slug(pg_slug=pg_slug)
        return result
