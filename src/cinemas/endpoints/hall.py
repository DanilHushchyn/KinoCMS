from django.http import HttpRequest
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_extra.pagination.decorator import paginate
from ninja_extra.schemas.response import PaginatedResponseSchema

from src.cinemas.models import Hall
from src.cinemas.schemas.hall import (HallInSchema,
                                      HallCardOutSchema,
                                      HallUpdateSchema,
                                      HallOutSchema, HallClientOutSchema)
from src.cinemas.services.hall import HallService
from src.core.errors import (NotFoundExceptionError,
                             UnprocessableEntityExceptionError,
                             NotUniqueFieldExceptionError,
                             InvalidTokenExceptionError)
from src.core.models import Image
from src.core.schemas.base import (LangEnum, MessageOutSchema,
                                   errors_to_docs)
from ninja_extra.permissions import IsAdminUser
from ninja_extra import http_get, http_post, http_patch, http_delete
from ninja import Header
from django.utils.translation import gettext as _

from src.core.utils import CustomJWTAuth


@api_controller("/hall", tags=["halls"])
class HallController(ControllerBase):
    """
    A controller class for managing hall in system.

    This class provides endpoints for
    get, post, update, delete hall in the admin site
    """

    def __init__(self, hall_service: HallService):
        """
        Use this method to inject "services" to HallController.

        :param hall_service: variable for managing halls
        """
        self.hall_service = hall_service

    @http_get(
        "/all-cards/",
        response=PaginatedResponseSchema[HallCardOutSchema],
        openapi_extra={
            "operationId": "get_all_hall_cards",
            "responses": errors_to_docs({
                404: [
                    NotFoundExceptionError(cls_model=Hall)
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    @paginate()
    def get_all_hall_cards(
            self,
            request: HttpRequest,
            cnm_slug: str,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> Hall:
        """
        Get all hall cards.

        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.hall_service.get_all(cnm_slug=cnm_slug)
        return result

    @http_post(
        "/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "create_hall",
            "responses": errors_to_docs({
                401: [
                    InvalidTokenExceptionError()
                ],
                404: [
                    NotFoundExceptionError(cls_model=Hall)
                ],
                409: [
                    NotUniqueFieldExceptionError(field='number')
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def create_hall(
            self,
            request: HttpRequest,
            body: HallInSchema,
            cnm_slug: str,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Create hall.

        Please provide:
          - **body**  body for creating new hall

        Returns:
          - **200**: Success response with the data.
          - **409**: Error: Conflict.
            Причини: \n
                1) Поле name повинно бути унікальним. Ця назва вже зайнята
          - **422**: Error: Unprocessable Entity. \n
            Причини: \n
                1) Максимальни довжина description 20_000 символів \n
                2) Максимальни довжина number 60 символів \n
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
        result = self.hall_service.create(schema=body, cnm_slug=cnm_slug)
        return result

    @http_patch(
        "/{hall_id}/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "update_hall",
            "responses": errors_to_docs({
                401: [
                    InvalidTokenExceptionError()
                ],
                404: [
                    NotFoundExceptionError(cls_model=Hall),
                    NotFoundExceptionError(cls_model=Image)
                ],
                409: [
                    NotUniqueFieldExceptionError(field='number')
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def update_hall(
            self,
            request: HttpRequest,
            hall_id: int,
            body: HallUpdateSchema,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Update hall.

        Please provide:
          - **body**  body for creating new hall

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Found. \n
            Причини: \n
                1) Не знайдено: немає збігів залів
                   на заданному запиті. \n
                2) Не знайдено: немає збігів картинок
                   на заданному запиті. \n
          - **409**: Error: Conflict. \n
            Причини: \n
                1) Поле name повинно бути унікальним. Ця назва вже зайнята
          - **422**: Error: Unprocessable Entity. \n
            Причини: \n
                1) Максимальни довжина description 20_000 символів \n
                2) Максимальни довжина number 60 символів \n
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
        self.hall_service.update(hall_id=hall_id, schema=body)
        return MessageOutSchema(detail=_('Зал успішно оновлений'))

    @http_get(
        "/{hall_id}/",
        response=HallOutSchema,
        openapi_extra={
            "operationId": "get_hall_by_id",
            "responses": errors_to_docs({
                404: [
                    NotFoundExceptionError(cls_model=Hall)
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def get_hall_by_id(
            self,
            request: HttpRequest,
            hall_id: int,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> Hall:
        """
        Create hall.

        Please provide:
          - **hall_id**  id of hall

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Not Found. \n
            Причини: \n
                1) Не знайдено: немає збігів залів
                   на заданному запиті. \n
                2) Не знайдено: немає збігів картинок
                   на заданному запиті. \n
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.hall_service.get_by_id(hall_id=hall_id)
        return result

    @http_delete(
        "/{hall_id}/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "delete_hall_by_slug",
            "responses": errors_to_docs({
                401: [
                    InvalidTokenExceptionError()
                ],
                404: [
                    NotFoundExceptionError(cls_model=Hall)
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def delete_hall_by_slug(
            self,
            request: HttpRequest,
            hall_id: int,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Delete hall by id.

        Please provide:
          - **hall_id**  id of hall

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Forbidden. \n
            Причини: \n
                1) Не знайдено: немає збігів залів
                   на заданному запиті. \n
                2) Не знайдено: немає збігів картинок
                   на заданному запиті. \n
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.hall_service.delete_by_id(hall_id=hall_id)
        return result


@api_controller("/hall", tags=["halls"])
class HallClientController(ControllerBase):
    """
    A controller class for managing hall in system.

    This class provides endpoints for
    get, hall in the client site
    """

    def __init__(self, hall_service: HallService):
        """
        Use this method to inject "services" to HallClientController.

        :param hall_service: variable for managing halls
        """
        self.hall_service = hall_service

    get_all_hall_cards = HallController.get_all_hall_cards

    @http_get(
        "/{hall_id}/",
        response=HallClientOutSchema,
        openapi_extra={
            "operationId": "get_hall_by_id",
            "responses": errors_to_docs({
                404: [
                    NotFoundExceptionError(cls_model=Hall)
                ],
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def get_hall_by_id(
            self,
            request: HttpRequest,
            hall_id: int,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> Hall:
        """
        Create hall.

        Please provide:
          - **hall_id**  id of hall

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Forbidden. \n
            Причини: \n
                1) Не знайдено: немає збігів залів
                   на заданному запиті. \n
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.hall_service.get_by_id(hall_id=hall_id)
        return result
