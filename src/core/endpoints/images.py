# Create your views here.
from typing import Optional

from django.contrib.sites.models import Site
from ninja import File
from ninja.files import UploadedFile
from django.http import HttpRequest
from ninja_extra.controllers.base import api_controller, ControllerBase

from config.settings.settings import MEDIA_URL, MEDIA_ROOT
from src.core.models import Image
from src.core.schemas.base import MessageOutSchema, LangEnum
from src.core.schemas.images import ImageOutSchema, ImageInSchema
from src.core.services.images import ImageService
from ninja_extra.permissions import IsAdminUser
from ninja_jwt.authentication import JWTAuth
from ninja_extra import http_delete, http_get, http_put, http_post, http_patch
from ninja import Header, Form
import loguru


@api_controller("/image", tags=["images"],)
class ImageController(ControllerBase):
    """
    A controller class for managing images in system.

    This class provides endpoints for
    get, post images in the site
    """

    def __init__(self, image_service: ImageService):
        """
        Use this method to inject "services" to ImageController.

        :param image_service: variable for managing images
        """
        self.image_service = image_service

    @http_post(
        "/upload/",
        response=ImageOutSchema,
        # permissions=[IsAdminUser()],
        # auth=JWTAuth(),
        openapi_extra={
            "responses": {
                403: {
                    "description": "Error: Forbidden",
                },
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
    def upload_image(
            self,
            request: HttpRequest,
            image: File[UploadedFile],
            body: Form[ImageInSchema],
            img_id: int = None,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> Image:
        """
        Create image for some entity.

        Please provide:
          - **file**  file for new template

        Returns:
          - **200**: Success response with the data.
          - **403**: Error: Forbidden. \n
              Причини:
              1) Максимально дозволений розмір файлу 1MB
              Причини:
              2) Максимально дозволена довжина поля alt 60 символів
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        # current_site = Site.objects.get_current(request).domain
        # current_site = Site.objects.get_current()
        # print(current_site)
        result = self.image_service.upload_image(alt=body.alt,
                                                 image=image,
                                                 img_id=img_id)
        return result

    @http_delete(
        "/{img_id}/",
        permissions=[IsAdminUser()],
        auth=JWTAuth(),
        response=MessageOutSchema,
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
    def delete_image(
            self,
            request: HttpRequest,
            img_id: int,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Create image for some entity.

        Please provide:
          - **img_id**  id for image for deleting

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Forbidden. \n
              Причини:
                1) Не знайдено: немає збігів картинок
                   на заданному запиті.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        # current_site = Site.objects.get_current(request).domain
        # current_site = Site.objects.get_current()
        # print(current_site)
        result = self.image_service.delete_image(img_id=img_id)
        return result

    @http_get(
        "/{img_id}/",
        response=ImageOutSchema,
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
    def get_image(
            self,
            request: HttpRequest,
            img_id: int,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> Image:
        """
        Ger image by id.

        Please provide:
          - **img_id**  id for image

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Forbidden. \n
              Причини:
                1) Не знайдено: немає збігів картинок
                   на заданному запиті.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        loguru.logger.debug(f"{ request.scheme }://{ request.META.get('HTTP_HOST') }")
        result = self.image_service.get_image(img_id=img_id)
        result.request = request
        return result
