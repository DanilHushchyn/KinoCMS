from django.utils.translation import gettext as _
from django.db import models

from src.core.errors import NotFoundExceptionError


# um1.User
class GalleryManager(models.Manager):
    """
    Custom user manager it's manager for making request to User model
    here is redefined some methods for saving
    user and superuser with email instead of username
    """

    def get_by_id(self, gallery_id: int) -> object:
        """
        Get an image with the given id.
        :param gallery_id: id of gallery
        :rtype: Gallery
        :return: Gallery model instance
        """
        try:
            gallery = self.model.objects.get(id=gallery_id)
        except self.model.DoesNotExist:
            msg = _('Не знайдено: немає збігів галерей '
                    'на заданному запиті.')
            raise NotFoundExceptionError(message=msg)
        return gallery
