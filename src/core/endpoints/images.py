# Create your views here.
from ninja import File
from ninja.files import UploadedFile
from django.http import HttpRequest
from ninja_extra.controllers.base import api_controller, ControllerBase

from src.core.schemas.base import MessageOutSchema, LangEnum
from src.core.schemas.images import ImageOutSchema
from src.core.services.images import ImageService
from ninja_extra.permissions import IsAdminUser
from ninja_jwt.authentication import JWTAuth
from ninja_extra import http_delete, http_get, http_patch, http_post
from ninja import Header, Form
import loguru


@api_controller("/images", tags=["images"],
                # permissions=[IsAdminUser()],
                # auth=JWTAuth()
                )
class ImageController(ControllerBase):
    """
    A controller class for managing images in system.

    This class provides endpoints for
    get, post images in the site
    """

    def __init__(self, image_service: ImageService, ):
        """
        Use this method to inject "services" to ImageController.

        :param image_service: variable for managing images
        """
        self.image_service = image_service

    @http_post(
        "/upload/",
        response=ImageOutSchema,
        openapi_extra={
            "responses": {
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
    def upload_image(
            self,
            request: HttpRequest,
            alt: Form[str],
            image: File[UploadedFile],
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> ImageOutSchema:
        """
        Create image for some entity.

        Please provide:
          - **file**  file for new template

        Returns:
          - **200**: Success response with the data.
          - **403**: Error: Forbidden. \n
              Причини:
              1) Максимально дозволений розмір файлу 1MB
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """

        result = self.image_service.upload_image(alt=alt, image=image)
        return result
