from datetime import datetime
from typing import TYPE_CHECKING

from django.db.models import QuerySet, Q
from ninja.errors import HttpError
from django.utils.translation import gettext as _
from django.db import models
from src.booking.models import Seance
from django.utils import timezone

if TYPE_CHECKING:
    from src.movies.models import Movie


# um1.User
class MovieManager(models.Manager):
    """
    Custom movie manager. It's manager for making request to Movie model
    here is redefined some methods for managing movies in system
    """

    def get_by_slug(self, mv_slug: str) -> 'Movie':
        """
        Get movie with the given slug.
        :param mv_slug: slug of movie
        :return:  model instance
        """
        try:
            movie = (self.model.objects
                     .select_related('card_img',
                                     'seo_image', 'gallery')
                     .prefetch_related('participants')
                     .get(slug=mv_slug))
        except self.model.DoesNotExist:
            msg = _('Не знайдено: немає збігів фільмів '
                    'на заданному запиті.')
            raise HttpError(404, msg)
        return movie

    def get_by_search_line(self, search_line: str) -> QuerySet['Movie']:
        """
        Get movie with the given search line.
        :param search_line: string for searching
        """
        movies = (self.model.objects
                  .select_related('card_img')
                  .filter(Q(name_ru__icontains=search_line) |
                          Q(name_uk__icontains=search_line)))
        return movies

    def get_today_movies(self, cnm_slug: str,
                         hall_id: int) -> QuerySet['Movie']:
        """
        Get movie with séances for today.
        """
        today = timezone.now()
        seances = Seance.objects.get_all().filter(date__date=today.date())
        if cnm_slug:
            from src.cinemas.models import Cinema
            cinema = Cinema.objects.get_by_slug(cnm_slug)
            seances = seances.filter(hall__cinema=cinema)
        if hall_id:
            from src.cinemas.models import Hall
            hall = Hall.objects.get_by_id(hall_id)
            seances = seances.filter(hall=hall)
        movie_ids = list(set(seances.values_list('movie_id', flat=True)))
        movies = self.model.objects.filter(id__in=movie_ids)
        return movies
