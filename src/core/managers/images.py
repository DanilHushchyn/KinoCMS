from django.utils.translation import gettext as _
from django.db import models
from typing import List
from src.core.errors import NotFoundExceptionError


class ImageManager(models.Manager):
    """
    Custom user manager it's manager for making request to User model
    here is redefined some methods for saving
    user and superuser with email instead of username
    """

    def get_by_id(self, img_id: int) -> object:
        """
        Get an image with the given id.
        :param img_id: id of image
        :rtype: Image
        :return: Image model instance
        """
        try:
            image = self.model.objects.get(id=img_id)
        except self.model.DoesNotExist:
            msg = _('Не знайдено: немає збігів картинок '
                    'на заданному запиті.')
            raise NotFoundExceptionError(message=msg)
        return image

    def check_of_ids(self, ids: List[int]) -> object:
        """
        Check that all values in parameter ids exist in db.
        :param ids: list of images ids
        :rtype: Boolean
        """
        db_ids = self.model.objects.values_list('id', flat=True)
        for i in ids:
            if i not in db_ids:
                msg = _('Не знайдено: немає збігів картинок '
                        'на заданному запиті.')
                raise NotFoundExceptionError(message=msg)
        return True
