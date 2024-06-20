from django.db.models import QuerySet
from django.http import HttpRequest
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_extra.pagination.decorator import paginate
from ninja_extra.schemas.response import PaginatedResponseSchema

from src.booking.models import Seance
from src.booking.schemas.seance import SeanceCardOutSchema
from src.booking.services.seance import SeanceService
from src.core.schemas.base import LangEnum, MessageOutSchema
from ninja_extra.permissions import IsAdminUser
from ninja_extra import http_get, http_post, http_patch, http_delete
from ninja import Header

from src.core.utils import CustomJWTAuth
from src.pages.models import Page
from src.pages.services.page import PageService


@api_controller("/seance", tags=["seances"])
class SeanceController(ControllerBase):
    """
    A controller class for managing séances in system.

    This class provides endpoints for
    get, post, update, delete séance in the site
    """

    def __init__(self, seance_service: SeanceService):
        """
        Use this method to inject "services" to SeanceController.

        :param seance_service: variable for managing pages
        """
        self.seance_service = seance_service

    @http_get(
        "/all/",
        response=PaginatedResponseSchema[SeanceCardOutSchema],
        openapi_extra={
            "operationId": "get_all_seances",
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
    def get_all_seances(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> QuerySet[Seance]:
        """
        Get all séances cards.

        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.seance_service.get_all()
        return result
