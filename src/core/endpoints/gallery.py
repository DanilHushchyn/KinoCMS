"""Gallery endpoints"""

from django.http import HttpRequest
from ninja import Header
from ninja_extra import http_get
from ninja_extra.controllers.base import ControllerBase
from ninja_extra.controllers.base import api_controller

from src.core.errors import NotFoundExceptionError
from src.core.errors import UnprocessableEntityExceptionError
from src.core.models import Gallery
from src.core.schemas.base import LangEnum
from src.core.schemas.base import errors_to_docs
from src.core.schemas.gallery import GalleryItemOutSchema
from src.core.services.gallery import GalleryService


@api_controller("/gallery", tags=["galleries"])
class GalleryController(ControllerBase):
    """A controller class for managing gallery in system.

    This class provides endpoints for
    get, post gallery in the site
    """

    def __init__(self, gallery_service: GalleryService):
        """Use this method to inject "services" to ImageController.

        :param gallery_service: variable for managing galleries
        """
        self.gallery_service = gallery_service

    @http_get(
        "/{gallery_id}/",
        response=list[GalleryItemOutSchema],
        openapi_extra={
            "operationId": "get_gallery_by_id",
            "responses": errors_to_docs(
                {
                    404: [NotFoundExceptionError(cls_model=Gallery)],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_gallery_by_id(
        self,
        request: HttpRequest,
        gallery_id: int,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> Gallery:
        """Get maximum of gallery fields.

        Please provide:
          - **gallery_id**  id of gallery we want to get

        Returns
        -------
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
