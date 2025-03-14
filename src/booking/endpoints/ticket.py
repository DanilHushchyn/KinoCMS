"""Endpoints for tickets"""

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Header
from ninja_extra import http_get
from ninja_extra import http_post
from ninja_extra.controllers.base import ControllerBase
from ninja_extra.controllers.base import api_controller

from src.booking.models import Seance
from src.booking.models import Ticket
from src.booking.schemas.ticket import BuyTicketSchema
from src.booking.schemas.ticket import TicketSchema
from src.booking.services.ticket import TicketService
from src.core.errors import NotFoundExceptionError
from src.core.errors import SmthWWExceptionError
from src.core.errors import TicketAlreadyBoughtExceptionError
from src.core.errors import UnprocessableEntityExceptionError
from src.core.schemas.base import LangEnum
from src.core.schemas.base import MessageOutSchema
from src.core.schemas.base import errors_to_docs


@api_controller("/ticket", tags=["tickets"])
class TicketController(ControllerBase):
    """A controller class for managing tickets in system.

    This class provides endpoints for
    get, post, delete tickets in the site
    """

    def __init__(self, ticket_service: TicketService):
        """Use this method to inject "services" to TicketController.

        :param ticket_service: variable for managing tikets
        """
        self.ticket_service = ticket_service

    @http_get(
        "/all/",
        response=list[TicketSchema],
        openapi_extra={
            "operationId": "get_tickets",
            "responses": errors_to_docs(
                {
                    404: [NotFoundExceptionError(cls_model=Seance)],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_tickets(
        self,
        request: HttpRequest,
        seance_id: int,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> QuerySet[Ticket]:
        """Get all tickets for séance by its id.

        Returns
        -------
          - **200**: Success response with the data.
          - **404**: Success response with the data.
          - **422**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        return self.ticket_service.get_tickets(seance_id=seance_id)

    @http_get(
        "/recently-bought/",
        response=list[TicketSchema],
        summary="Get recent tickets (Long polling)",
        openapi_extra={
            "operationId": "get_recently_tickets",
            "responses": errors_to_docs(
                {
                    404: [NotFoundExceptionError(cls_model=Seance)],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_recently_tickets(
        self,
        request: HttpRequest,
        seance_id: int,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> QuerySet[Ticket]:
        """Get all tickets that has been bought recently.
        Long polling endpoint

        Returns
        -------
          - **200**: Success response with the data.
          - **404**: Success response with the data.
            Причини: \n
                1) Не знайдено: немає збігів сеансів \n
                   на заданному запиті.
          - **422**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        return self.ticket_service.get_recently_tickets(seance_id=seance_id)

    @http_post(
        "/buy/",
        response=MessageOutSchema,
        openapi_extra={
            "operationId": "buy_ticket",
            "responses": errors_to_docs(
                {
                    402: [SmthWWExceptionError()],
                    404: [NotFoundExceptionError(cls_model=Seance)],
                    409: [TicketAlreadyBoughtExceptionError()],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def buy_tickets(
        self,
        request: HttpRequest,
        payload: BuyTicketSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> MessageOutSchema:
        """Buy ticket to séance.
        Please provide:
          - **Request body**  data for booking tickets

        Returns
        -------
          - **200**: Success response with the data.
          - **402**: Success response with the data.
            Причини: \n
                1) Операція з оплатою нажаль не пройшла, \n
                   спробуйте ще раз.
          - **404**: Success response with the data.
            Причини: \n
                1) Не знайдено: немає збігів сеансів \n
                   на заданному запиті.
          - **409**: Error: Conflict. \n
            Причини: \n
                1) У вказаному переліку квитків \n
                   є ті які вже кимось придбані
          - **422**: Success response with the data.
            Причини: \n
                1) Дані про розташування \n
                   квитка на схемі неправельні. \n
                2) Квитки для покупки не обрані, \n
                   має бути мінімум 1.\n
          - **500**: Internal server error if an unexpected error occurs.

        """
        return self.ticket_service.buy_tickets(payload=payload)
