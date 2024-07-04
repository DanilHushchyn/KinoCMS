from typing import TYPE_CHECKING

from django.db.models import QuerySet, Q, Count, F
from django.utils.translation import gettext as _
from django.db import models
from src.booking.models import Seance
from django.utils import timezone

from src.core.errors import NotFoundExceptionError

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
                     .prefetch_related('participants__role')
                     .prefetch_related('participants__person')
                     .get(slug=mv_slug))
        except self.model.DoesNotExist:
            msg = _('Не знайдено: немає збігів фільмів '
                    'на заданному запиті.')
            raise NotFoundExceptionError(message=msg, cls_model=self.model)
        from src.movies.models import MovieParticipantRole, MovieParticipantPerson

        mv_roles = MovieParticipantRole.objects.filter(movieparticipant__movie=movie).distinct()
        for mv_role in mv_roles:
            persons_list = []
            for participant in movie.participants.all():
                if participant.role == mv_role:
                    persons_list.append(participant.person.fullname)
            mv_role.persons = persons_list
        movie.mv_roles = mv_roles
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

    def get_today_movies(self) -> QuerySet['Movie']:
        """
        Get movie with séances for today.
        """
        today = timezone.now()
        seances = Seance.objects.get_all().filter(date__date=today.date())
        movie_ids = list(set(seances.values_list('movie_id', flat=True)))
        movies = self.model.objects.filter(id__in=movie_ids)
        return movies
