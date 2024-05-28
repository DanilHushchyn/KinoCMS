from typing import TYPE_CHECKING

from ninja.errors import HttpError
from django.utils.translation import gettext as _
from django.db import models
if TYPE_CHECKING:
    from src.cinemas.models import Cinema


# um1.User
class CinemaManager(models.Manager):
    """
    Custom cinema manager. It's manager for making request to Cinema model
    here is redefined some methods for managing cinemas in system
    """

    def get_by_slug(self, cnm_slug: str) -> 'Cinema':
        """
        Get cinema with the given id.
        :param cnm_slug: slug of cinema
        :rtype: Cinema
        :return: Cinema model instance
        """
        try:
            cinema = self.model.objects.get(slug=cnm_slug)
        except self.model.DoesNotExist:
            msg = _('Не знайдено: немає збігів кінотеатрів '
                    'на заданному запиті.')
            raise HttpError(403, msg)
        return cinema
