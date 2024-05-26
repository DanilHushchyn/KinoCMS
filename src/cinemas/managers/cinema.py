from ninja.errors import HttpError
from django.utils.translation import gettext as _
from django.db import models


# um1.User
class CinemaManager(models.Manager):
    """
    Custom cinema manager. It's manager for making request to Cinema model
    here is redefined some methods for managing cinemas in system
    """

    def get_by_id(self, cinema_id: int) -> object:
        """
        Get cinema with the given id.
        :param cinema_id: id of cinema
        :rtype: Cinema
        :return: Cinema model instance
        """
        try:
            cinema = self.model.objects.get(id=cinema_id)
        except self.model.DoesNotExist:
            msg = _('Не знайдено: немає збігів кінотеатрів '
                    'на заданному запиті.')
            raise HttpError(403, msg)
        return cinema
