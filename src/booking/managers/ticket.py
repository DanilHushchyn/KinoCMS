import random
from typing import TYPE_CHECKING
from django.db.models import QuerySet
from django.utils.translation import gettext as _
from django.db import models, IntegrityError
from src.booking.schemas.ticket import BuyTicketSchema
from src.core.errors import (NotFoundExceptionError,
                             TicketAlreadyBoughtExceptionError,
                             UnprocessableEntityExceptionError,
                             SmthWWExceptionError)
from src.core.schemas.base import MessageOutSchema
from django.utils import timezone
if TYPE_CHECKING:
    from src.booking.models import Ticket, Seance


# um1.User
class TicketManager(models.Manager):
    """
    Custom ticket manager. It's manager for making request to Ticket model
    here is redefined some methods for managing tickets in system
    """

    def get_tickets_by_seance_id(self, seance_id: int) \
            -> QuerySet['Ticket']:
        """
        Get séance with the given id.
        :param seance_id: if of séance
        :return: Séance model instance
        """
        from src.booking.models import Seance
        try:
            seance = (Seance.objects
                      .prefetch_related('ticket_set')
                      .get(id=seance_id))
        except Seance.DoesNotExist:
            msg = _('Не знайдено: немає збігів сеансів '
                    'на заданному запиті.')
            raise NotFoundExceptionError(message=msg, cls_model=Seance)
        return seance.ticket_set.all()

    def create_tickets(self, payload: BuyTicketSchema) \
            -> MessageOutSchema:
        """
        Get séance with the given id.
        :param payload: body for creating ticket
        """
        from src.booking.models import Seance

        try:
            today = timezone.now()
            seance = (Seance.objects.prefetch_related('hall')
                      .get(id=payload.seance_id, date__gte=today))
        except Seance.DoesNotExist:
            msg = _('Не знайдено: немає збігів сеансів '
                    'на заданному запиті.')
            raise NotFoundExceptionError(message=msg, cls_model=Seance)
        tickets = []
        for ticket in payload.tickets:
            found = False
            for row in seance.hall.layout['rows']:
                if 'number' in row and row['number'] == ticket.row:
                    for seat in row['seats']:
                        if ('number' in seat and
                                seat['number'] == ticket.seat):
                            found = True
            if found is False:
                msg = _(f'Дані про розташування '
                        f'квитка (ряд: {ticket.row}, '
                        f'місце: {ticket.seat}) '
                        f'на схемі неправельні.')
                raise UnprocessableEntityExceptionError(message=msg)
            item = self.model(seance_id=payload.seance_id,
                              row=ticket.row,
                              seat=ticket.seat)
            tickets.append(item)
        if len(tickets) < 1:
            msg = _('Квитки для покупки не обрані, має бути мінімум 1.')
            raise UnprocessableEntityExceptionError(message=msg,
                                                    field='tickets')
        try:
            tickets_list = self.model.objects.bulk_create(tickets)
        except IntegrityError:
            if len(tickets) > 1:
                msg = _("У вказаному переліку квитків "
                        "є ті які вже кимось придбані")
            else:
                msg = _("Цей квиток вже придбаний кимось")
            raise TicketAlreadyBoughtExceptionError(message=msg)
        if random.choice([False, False, True]):
            ticket_ids = [ticket.id for ticket in tickets_list]
            queryset = self.model.objects.filter(id__in=ticket_ids)
            queryset.delete()
            msg = _('Операція з оплатою нажаль не пройшла, '
                    'спробуйте ще раз.')
            raise SmthWWExceptionError(message=msg)
        msg = _('Покупка пройшла успішно')

        return MessageOutSchema(detail=msg)
