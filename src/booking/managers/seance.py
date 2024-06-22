from datetime import datetime
from typing import TYPE_CHECKING

from django.db.models import QuerySet
from django.utils.timezone import make_aware
from django.utils import timezone
from ninja.errors import HttpError
from django.utils.translation import gettext as _
from django.db import models

if TYPE_CHECKING:
    from src.booking.models import Seance


# um1.User
class SeanceManager(models.Manager):
    """
    Custom séance manager. It's manager for making request to Séance model
    here is redefined some methods for managing séances in system
    """

    def get_by_id(self, seance_id: int) -> 'Seance':
        """
        Get séance with the given id.
        :param seance_id: if of séance
        :return: Séance model instance
        """
        try:
            seance = (self.model.objects
                      .prefetch_related('movie__card_img', 'hall')
                      .get(id=seance_id))
        except self.model.DoesNotExist:
            msg = _('Не знайдено: немає збігів сеансів '
                    'на заданному запиті.')
            raise HttpError(404, msg)
        return seance

    def get_all(self) -> QuerySet['Seance']:
        """
        Get all séances in site.
        :return: Séance model instance
        """
        today = timezone.now()
        seances = (self.model.objects
                   .filter(date__gte=today))
        return seances

    def get_all_expired(self) -> QuerySet['Seance']:
        """
        Get all expired séances in site.
        :return: Séance model instance
        """
        today = timezone.now()
        seances = (self.model.objects.prefetch_related('ticket_set')
                   .exclude(date__gte=today))
        return seances
