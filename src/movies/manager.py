from typing import TYPE_CHECKING

from ninja.errors import HttpError
from django.utils.translation import gettext as _
from django.db import models

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
