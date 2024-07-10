from datetime import timedelta
from typing import TYPE_CHECKING
from django.db.models import QuerySet, Q
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db import models
from django.template.defaultfilters import date as _date
from django.utils import translation
import pymorphy2

from src.core.errors import NotFoundExceptionError

if TYPE_CHECKING:
    from src.booking.schemas.seance import SeanceFilterSchema
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
            today = timezone.now()
            seance = (self.model.objects
                      .select_related('movie__card_img',
                                      'hall__banner')
                      .get(id=seance_id, date__gte=today))

        except self.model.DoesNotExist:
            msg = _('Не знайдено: немає збігів сеансів '
                    'на заданному запиті.')
            raise NotFoundExceptionError(message=msg, cls_model=self.model)

        return seance

    def get_all(self) -> QuerySet['Seance']:
        """
        Get all séances in site.
        :return: Séance model instance
        """
        today = timezone.now()
        seances = (self.model.objects
                   .filter(date__date__gte=today.date()))
        return seances

    def get_filtered(self, filters: 'SeanceFilterSchema') -> list:
        """
        Get all séances in site.
        :return: Séance model instance
        """
        today = timezone.now()
        tomorrow = timezone.now() + timedelta(days=1)
        seances = (self.model.objects
                   .prefetch_related('movie',
                                     'hall__cinema',
                                     'ticket_set')
                   .filter(date__date__gte=today.date()))
        seances = seances.filter(hall__cinema__slug=filters.cnm_slug)
        if filters.hall_ids:
            seances = seances.filter(hall__id__in=filters.hall_ids)
        if filters.mv_slugs:
            seances = seances.filter(movie__slug__in=filters.mv_slugs)
        if filters.tech_ids:
            seances = seances.filter(hall__tech__in=filters.tech_ids)
        if filters.date:
            seances = seances.filter(date__date=filters.date)
            dates = [filters.date]
        else:
            seances = seances.filter(Q(date__date=today.date()) |
                                     Q(date__date=tomorrow.date()))
            dates = [today.date(), tomorrow.date()]
        result = []
        for date in dates:
            date_seances = []
            for seance in seances:
                if seance.date.date() == date:
                    date_seances.append(seance)
            date = _date(date, 'd F l')
            date = date.split(' ')
            current_lang = translation.get_language()
            morph = pymorphy2.MorphAnalyzer(lang=current_lang)
            parser = morph.parse(date[1])[0]
            gent = parser.inflect({'gent'})
            date[1] = gent.word + ','
            result.append({
                'date': ' '.join(date).upper(),
                'seances': date_seances,

            })
        return result

    def get_all_expired(self) -> QuerySet['Seance']:
        """
        Get all expired séances in site.
        :return: Séance model instance
        """
        today = timezone.now()
        seances = (self.model.objects.prefetch_related('ticket_set')
                   .exclude(date__date__gte=today.date()))
        return seances

    def get_today_seances(self, cnm_slug: str,
                          hall_id: int) -> QuerySet['Seance']:
        """
        Get séances for today.
        """
        today = timezone.now()
        seances = (self.model.objects.filter(date__gte=today)
                   .filter(date__date=today.date()))
        if cnm_slug:
            from src.cinemas.models import Cinema
            cinema = Cinema.objects.get_by_slug(cnm_slug)
            seances = seances.filter(hall__cinema=cinema)
        if hall_id:
            from src.cinemas.models import Hall
            hall = Hall.objects.get_by_id(hall_id)
            seances = seances.filter(hall=hall)
        return seances
