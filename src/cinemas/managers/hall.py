from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext as _

from src.core.errors import NotFoundExceptionError

if TYPE_CHECKING:
    from src.cinemas.models import Hall


class HallManager(models.Manager):
    """Custom hall manager. It's manager for making request to Hall model
    here is redefined some methods for managing halls in system
    """

    def get_by_id(self, hall_id: int) -> "Hall":
        """Get hall with the given id.
        :param hall_id: id of hall
        :rtype: Hall
        :return: Hall model instance
        """
        try:
            hall = self.model.objects.select_related(
                "banner", "seo_image", "gallery", "cinema"
            ).get(id=hall_id)
        except self.model.DoesNotExist:
            msg = _("Не знайдено: немає збігів залів " "на заданному запиті.")
            raise NotFoundExceptionError(message=msg, cls_model=self.model)
        return hall

    def get_schema(self, hall_id: int) -> "Hall":
        """Get hall schema with the given hall id.
        :param hall_id: id of hall
        :rtype: Hall
        :return: Hall model instance
        """
        try:
            hall = self.model.objects.only("layout").get(id=hall_id)
        except self.model.DoesNotExist:
            msg = _("Не знайдено: немає збігів залів " "на заданному запиті.")
            raise NotFoundExceptionError(message=msg, cls_model=self.model)
        return hall
