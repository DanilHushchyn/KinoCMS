from typing import TYPE_CHECKING
from django.utils.translation import gettext as _
from django.db import models
from src.core.errors import NotFoundExceptionError

if TYPE_CHECKING:
    from src.pages.models import BottomSliderItem


# um1.User
class BottomSliderItemManager(models.Manager):
    """
    Custom cinema manager. It's manager for making request to Cinema model
    here is redefined some methods for managing cinemas in system
    """

    def get_by_id(self, slider_id: int) -> 'BottomSliderItem':
        """
        Get cinema with the given id.
        :param slider_id: id of bottom slider's item
        :return: BottomSliderItem model instance
        """
        try:
            slider = (self.model.objects.get(id=slider_id))
        except self.model.DoesNotExist:
            msg = _('Не знайдено: немає збігів елементів '
                    'нижнього банеру '
                    'на заданному запиті.')
            raise NotFoundExceptionError(message=msg, cls_model=self.model)
        return slider
