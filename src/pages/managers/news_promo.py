from typing import TYPE_CHECKING
from django.utils.translation import gettext as _
from django.db import models

from src.core.errors import NotFoundExceptionError

if TYPE_CHECKING:
    from src.pages.models import NewsPromo


# um1.User
class NewsPromoManager(models.Manager):
    """
    Custom news_promo manager. It's manager
    for making request to NewsPromo model
    here is redefined some methods
    for managing news_promos in system
    """

    def get_by_slug(self, np_slug: str) -> 'NewsPromo':
        """
        Get news_promo with the given slug.
        :param np_slug: slug of news_promo
        :return: NewsPromo model instance
        """
        try:
            news_promo = (self.model.objects
                          .select_related('seo_image',
                                          'banner', 'gallery')
                          .get(slug=np_slug))
        except self.model.DoesNotExist:
            msg = _('Не знайдено: немає збігів новин чи акцій '
                    'на заданному запиті.')
            raise NotFoundExceptionError(message=msg, cls_model=self.model)
        return news_promo
