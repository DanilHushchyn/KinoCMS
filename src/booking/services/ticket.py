from datetime import timedelta

from django.db.models import QuerySet
from django.utils import timezone

from src.booking.models import Ticket
from src.booking.schemas.ticket import BuyTicketSchema
from src.core.schemas.base import MessageOutSchema


class TicketService:
    """A service class for managing tickets."""

    @staticmethod
    def buy_tickets(payload: BuyTicketSchema) -> MessageOutSchema:
        """Buy ticket to séance.
        :param payload: contains data for booking tickets

        """
        result = Ticket.objects.create_tickets(payload=payload)
        return result

    @staticmethod
    def get_tickets(seance_id: int) -> QuerySet[Ticket]:
        """Get tickets by séance id.
        :param seance_id: id of séance
        """
        result = Ticket.objects.get_tickets_by_seance_id(seance_id=seance_id)
        return result

    @staticmethod
    def get_recently_tickets(seance_id: int) -> QuerySet[Ticket]:
        """Get tickets by séance id.
        :param seance_id: id of séance
        """
        today = timezone.now()
        today = today - timedelta(minutes=1)
        tickets = Ticket.objects.filter(seance_id=seance_id, date_created__gte=today)
        return tickets
