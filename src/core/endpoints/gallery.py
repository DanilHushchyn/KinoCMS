# Create your views here.
from typing import List

from django.http import HttpRequest
from ninja_extra.controllers.base import api_controller, ControllerBase

from src.core.models import Gallery
from src.core.schemas.base import LangEnum
from src.core.schemas.gallery import GalleryInSchema, GalleryMinOutSchema, GalleryOutSchema, GalleryItemOutSchema
from src.core.schemas.images import ImageOutSchema
from src.core.services.gallery import GalleryService
from ninja_extra.permissions import IsAdminUser
from ninja_jwt.authentication import JWTAuth
from ninja_extra import http_get, http_post, http_patch
from ninja import Header


@api_controller("/gallery", tags=["galleries"])
class GalleryController(ControllerBase):
    """
    A controller class for managing gallery in system.

    This class provides endpoints for
    get, post gallery in the site
    """

    def __init__(self, gallery_service: GalleryService):
        """
        Use this method to inject "services" to ImageController.

        :param gallery_service: variable for managing galleries
        """
        self.gallery_service = gallery_service

    @http_get(
        "/{gallery_id}/",
        response=List[GalleryItemOutSchema],
        # permissions=[IsAdminUser()],
        # auth=JWTAuth(),
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
    def get_gallery(
            self,
            request: HttpRequest,
            gallery_id: int,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> Gallery:
        """
        Get maximum of gallery fields.

        Please provide:
          - **gallery_id**  id of gallery we want to get

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Not Found. \n
              Причини:
                1) Не знайдено: немає збігів галерей
                   на заданному запиті.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.gallery_service.get_by_id(gallery_id=gallery_id)
        return result

    # @http_delete(
    #     "/{img_id}/",
    #     permissions=[IsAdminUser()],
    #     auth=JWTAuth(),
    #     response=MessageOutSchema,
    #     openapi_extra={
    #         "responses": {
    #             404: {
    #                 "description": "Error: Not Found",
    #             },
    #             422: {
    #                 "description": "Error: Unprocessable Entity",
    #             },
    #             500: {
    #                 "description": "Internal server error "
    #                                "if an unexpected error occurs.",
    #             },
    #         },
    #     },
    # )
    # def delete_image(
    #         self,
    #         request: HttpRequest,
    #         img_id: int,
    #         accept_lang: LangEnum =
    #         Header(alias="Accept-Language",
    #                default="uk"),
    # ) -> MessageOutSchema:
    #     """
    #     Create image for some entity.
    #
    #     Please provide:
    #       - **img_id**  id for image for deleting
    #
    #     Returns:
    #       - **200**: Success response with the data.
    #       - **404**: Error: Forbidden. \n
    #           Причини:
    #             1) Не знайдено: немає збігів картинок
    #                на заданному запиті.
    #       - **422**: Error: Unprocessable Entity.
    #       - **500**: Internal server error if an unexpected error occurs.
    #     """
    #     # current_site = Site.objects.get_current(request).domain
    #     # current_site = Site.objects.get_current()
    #     # print(current_site)
    #     result = self.image_service.delete_image(img_id=img_id)
    #     return result
    #
    # @http_get(
    #     "/{img_id}/",
    #     response=ImageOutSchema,
    #     openapi_extra={
    #         "responses": {
    #             404: {
    #                 "description": "Error: Not Found",
    #             },
    #             422: {
    #                 "description": "Error: Unprocessable Entity",
    #             },
    #             500: {
    #                 "description": "Internal server error "
    #                                "if an unexpected error occurs.",
    #             },
    #         },
    #     },
    # )
    # def get_image(
    #         self,
    #         request: HttpRequest,
    #         img_id: int,
    #         accept_lang: LangEnum =
    #         Header(alias="Accept-Language",
    #                default="uk"),
    # ) -> Image:
    #     """
    #     Ger image by id.
    #
    #     Please provide:
    #       - **img_id**  id for image
    #
    #     Returns:
    #       - **200**: Success response with the data.
    #       - **404**: Error: Forbidden. \n
    #           Причини:
    #             1) Не знайдено: немає збігів картинок
    #                на заданному запиті.
    #       - **422**: Error: Unprocessable Entity.
    #       - **500**: Internal server error if an unexpected error occurs.
    #     """
    #     # current_site = Site.objects.get_current(request).domain
    #     # current_site = Site.objects.get_current()
    #     # print(current_site)
    #     result = self.image_service.get_image(img_id=img_id)
    #     return result
