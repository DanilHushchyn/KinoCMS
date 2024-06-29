from typing import TYPE_CHECKING
from django.utils.translation import gettext as _
from django.db import models

from src.core.errors import NotFoundExceptionError

if TYPE_CHECKING:
    from src.pages.models import Page


# um1.User
class PageManager(models.Manager):
    """
    Custom page manager. It's manager
    for making request to Page model
    here is redefined some methods
    for managing pages in system
    """

    def get_by_slug(self, pg_slug: str) -> 'Page':
        """
        Get page with the given slug.
        :param pg_slug: slug of page
        """
        try:
            page = (self.model.objects
                    .select_related('seo_image',
                                    'banner', 'gallery')
                    .get(slug=pg_slug))
        except self.model.DoesNotExist:
            msg = _('Не знайдено: немає збігів сторінок '
                    'на заданному запиті.')
            raise NotFoundExceptionError(message=msg, cls_model=self.model)
        return page
