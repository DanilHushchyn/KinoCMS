"""Endpoints for séances"""

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Header
from ninja import Query
from ninja_extra import http_get
from ninja_extra.controllers.base import ControllerBase
from ninja_extra.controllers.base import api_controller
from ninja_extra.pagination.decorator import paginate
from ninja_extra.schemas.response import PaginatedResponseSchema

from src.booking.models import Seance
from src.booking.schemas.seance import ScheduleOutSchema
from src.booking.schemas.seance import SeanceCardOutSchema
from src.booking.schemas.seance import SeanceFilterSchema
from src.booking.schemas.seance import SeanceShortSchema
from src.booking.services.seance import SeanceService
from src.core.errors import NotFoundExceptionError
from src.core.errors import UnprocessableEntityExceptionError
from src.core.schemas.base import LangEnum
from src.core.schemas.base import errors_to_docs


@api_controller("/seance", tags=["seances"])
class SeanceController(ControllerBase):
    """A controller class for managing séances in system.

    This class provides endpoints for
    get, post, update, delete séance in the site
    """

    def __init__(self, seance_service: SeanceService):
        """Use this method to inject "services" to SeanceController.

        :param seance_service: variable for managing pages
        """
        self.seance_service = seance_service

    @http_get(
        "/schedule/",
        response=list[ScheduleOutSchema],
        openapi_extra={
            "operationId": "get_schedule",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_schedule(
        self,
        request: HttpRequest,
        filters: SeanceFilterSchema = Query(...),
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> list:
        """Get all séances cards.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        return self.seance_service.get_filtered(filters=filters)

    @http_get(
        "/today-cards/",
        response=PaginatedResponseSchema[SeanceShortSchema],
        openapi_extra={
            "operationId": "get_today_seances",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    @paginate()
    def get_today_seances(
        self,
        request: HttpRequest,
        cnm_slug: str | None = None,
        hall_id: int | None = None,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> QuerySet[Seance]:
        """Search movies by search line.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        return self.seance_service.get_today_seances(cnm_slug=cnm_slug, hall_id=hall_id)

    @http_get(
        "/{seance_id}/",
        response=SeanceCardOutSchema,
        openapi_extra={
            "operationId": "get_seance_by_id",
            "responses": errors_to_docs(
                {
                    404: [NotFoundExceptionError(cls_model=Seance)],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_seance_by_id(
        self,
        request: HttpRequest,
        seance_id: int,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> Seance:
        """Get séance by id.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.seance_service.get_by_id(seance_id=seance_id)
        return result
