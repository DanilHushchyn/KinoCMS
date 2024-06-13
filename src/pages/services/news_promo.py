from src.pages.models import NewsPromo
from src.pages.schemas.news_promo import (NewsPromoInSchema,
                                          NewsPromoUpdateSchema)
from django.utils.translation import gettext as _
from pytils.translit import slugify

from src.core.schemas.base import MessageOutSchema
from src.core.services.core import CoreService
from src.core.services.gallery import GalleryService
from src.core.services.images import ImageService
from injector import inject


class NewsPromoService:
    """
    A service class for managing news_promo.
    """

    @inject
    def __init__(self,
                 image_service: ImageService,
                 core_service: CoreService,
                 gallery_service: GalleryService):
        self.image_service = image_service
        self.gallery_service = gallery_service
        self.core_service = core_service

    def create(self, schema: NewsPromoInSchema) -> MessageOutSchema:
        """
        Create news_promo.
        """
        self.core_service.check_name_unique(value=schema.name_uk,
                                            model=NewsPromo)
        self.core_service.check_name_unique(value=schema.name_ru,
                                            model=NewsPromo)
        bodies = [schema.banner, schema.seo_image]
        banner, seo_image = (self.image_service
                             .bulk_create(schemas=bodies))
        gallery = self.gallery_service.create(images=schema.gallery)

        news_promo = NewsPromo.objects.create(
            name_uk=schema.name_uk,
            name_ru=schema.name_ru,
            slug=slugify(schema.name_uk),
            description_uk=schema.description_uk,
            description_ru=schema.description_ru,
            banner=banner,
            promo=schema.promo,
            active=schema.active,
            video_link=schema.video_link,
            gallery=gallery,
            seo_title=schema.seo_title,
            seo_description=schema.seo_description,
            seo_image=seo_image,
        )
        if news_promo.promo:
            return MessageOutSchema(detail=_('Акція успішно створена'))
        return MessageOutSchema(detail=_('Новина успішно створена'))

    def update(self, np_slug: str, schema: NewsPromoUpdateSchema) \
            -> MessageOutSchema:
        """
        Update news_promo.
        """
        news_promo = NewsPromo.objects.get_by_slug(np_slug=np_slug)
        self.core_service.check_name_unique(value=schema.name_uk,
                                            instance=news_promo,
                                            model=NewsPromo)
        self.core_service.check_name_unique(value=schema.name_ru,
                                            instance=news_promo,
                                            model=NewsPromo)
        self.image_service.update(schema.banner, news_promo.banner)
        self.image_service.update(schema.seo_image, news_promo.seo_image)

        self.gallery_service.update(schemas=schema.gallery,
                                    gallery=news_promo.gallery)
        expt_list = ['banner', 'seo_image', 'gallery']
        for attr, value in schema.dict().items():
            if attr not in expt_list and value is not None:
                setattr(news_promo, attr, value)
        news_promo.slug = slugify(news_promo.name_uk)
        news_promo.save()
        if news_promo.promo:
            return MessageOutSchema(detail=_('Акція успішно оновлена'))
        return MessageOutSchema(detail=_('Новина успішно оновлена'))

    @staticmethod
    def get_by_slug(np_slug: str) -> NewsPromo:
        """
        Get news_promo by slug.
        """
        news_promo = NewsPromo.objects.get_by_slug(np_slug=np_slug)
        return news_promo

    @staticmethod
    def get_all(promo: bool) -> NewsPromo:
        """
        Get all news_promos.
        """
        if promo:
            news_promo = NewsPromo.objects.filter(promo=True)
        else:
            news_promo = NewsPromo.objects.filter(promo=False)
        return news_promo

    def delete_by_slug(self, np_slug: str) -> MessageOutSchema:
        """
        Delete news_promo.
        """
        news_promo = (NewsPromo.objects
                      .get_by_slug(np_slug=np_slug))
        promo = news_promo.promo
        np_imgs_ids = [news_promo.seo_image_id,
                       news_promo.banner_id, ]
        gallery = news_promo.gallery
        news_promo.delete()
        gallery_imgs_ids = list(gallery.images.values_list('id', flat=True))
        gallery.delete()
        imgs_ids_for_delete = np_imgs_ids + gallery_imgs_ids
        self.image_service.bulk_delete(imgs_ids_for_delete)
        if promo:
            return MessageOutSchema(detail=_('Акція успішно видалена'))
        return MessageOutSchema(detail=_('Новина успішно видалена'))
