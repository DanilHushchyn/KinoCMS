"""Service for managing news and promos"""

from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext as _
from injector import inject

from src.core.errors import NotFoundExceptionError
from src.core.schemas.base import MessageOutSchema
from src.core.services.core import CoreService
from src.core.services.gallery import GalleryService
from src.core.services.images import ImageService
from src.core.utils import make_slug
from src.pages.models import NewsPromo
from src.pages.models import Tag
from src.pages.schemas.news_promo import NewsPromoInSchema
from src.pages.schemas.news_promo import NewsPromoUpdateSchema


class NewsPromoService:
    """A service class for managing news_promo."""

    @inject
    def __init__(
        self,
        image_service: ImageService,
        core_service: CoreService,
        gallery_service: GalleryService,
    ):
        self.image_service = image_service
        self.gallery_service = gallery_service
        self.core_service = core_service

    def create(
        self, request: HttpRequest, schema: NewsPromoInSchema
    ) -> MessageOutSchema:
        """Create news_promo."""
        self.core_service.check_field_unique(
            value=schema.name_uk, field_name="name_uk", model=NewsPromo
        )
        self.core_service.check_field_unique(
            value=schema.name_ru, field_name="name_ru", model=NewsPromo
        )
        bodies = [schema.banner, schema.seo_image]
        banner, seo_image = self.image_service.bulk_create(schemas=bodies)
        gallery = self.gallery_service.create(images=schema.gallery)

        news_promo = NewsPromo.objects.create(
            name_uk=schema.name_uk,
            name_ru=schema.name_ru,
            slug=make_slug(value=schema.name_uk, model=NewsPromo),
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
        if schema.tags is not None:
            news_promo.tags.set(schema.tags)
        news_promo.save()
        if news_promo.promo:
            return MessageOutSchema(detail=_("Акція успішно створена"))
        return MessageOutSchema(detail=_("Новина успішно створена"))

    def update(
        self, request: HttpRequest, np_slug: str, schema: NewsPromoUpdateSchema
    ) -> MessageOutSchema:
        """Update news_promo."""
        news_promo = NewsPromo.objects.get_by_slug(np_slug=np_slug)
        self.core_service.check_field_unique(
            value=schema.name_uk,
            instance=news_promo,
            field_name="name_uk",
            model=NewsPromo,
        )
        self.core_service.check_field_unique(
            value=schema.name_ru,
            instance=news_promo,
            field_name="name_ru",
            model=NewsPromo,
        )
        self.image_service.update(schema.banner, news_promo.banner)
        self.image_service.update(schema.seo_image, news_promo.seo_image)

        self.gallery_service.update(schemas=schema.gallery, gallery=news_promo.gallery)
        expt_list = ["banner", "seo_image", "gallery", "tags"]
        for attr, value in schema.dict().items():
            if attr not in expt_list and value is not None:
                setattr(news_promo, attr, value)
        news_promo.slug = make_slug(
            value=news_promo.name_uk, model=NewsPromo, instance=news_promo
        )
        if schema.tags is not None:
            news_promo.tags.set(schema.tags)

        news_promo.save()
        if news_promo.promo:
            return MessageOutSchema(detail=_("Акція успішно оновлена"))
        return MessageOutSchema(detail=_("Новина успішно оновлена"))

    @staticmethod
    def get_by_slug(np_slug: str) -> NewsPromo:
        """Get news_promo by slug."""
        news_promo = NewsPromo.objects.get_by_slug(np_slug=np_slug)
        return news_promo

    @staticmethod
    def get_active_by_slug(np_slug: str) -> NewsPromo:
        """Get news or promo by slug."""
        news_promo = NewsPromo.objects.get_by_slug(np_slug=np_slug)
        if news_promo.active is False:
            msg = _("Не знайдено: немає збігів новин и акцій " "на заданному запиті.")
            raise NotFoundExceptionError(message=msg, cls_model=NewsPromo)
        return news_promo

    @staticmethod
    def get_all(promo: bool) -> NewsPromo:
        """Get all news_promos."""
        if promo:
            news_promo = NewsPromo.objects.filter(promo=True)
        else:
            news_promo = NewsPromo.objects.filter(promo=False)
        return news_promo

    @staticmethod
    def get_all_tags() -> QuerySet[Tag]:
        """Get all tags."""
        tags = Tag.objects.all()
        return tags

    @staticmethod
    def get_all_active(promo: bool) -> QuerySet[NewsPromo]:
        """Get all news_promos."""
        if promo:
            news_promo = NewsPromo.objects.prefetch_related("tags", "banner").filter(
                promo=True, active=True
            )
        else:
            news_promo = NewsPromo.objects.prefetch_related("tags", "banner").filter(
                promo=False, active=True
            )

        return news_promo

    def delete_by_slug(self, np_slug: str) -> MessageOutSchema:
        """Delete news_promo."""
        news_promo = NewsPromo.objects.get_by_slug(np_slug=np_slug)
        promo = news_promo.promo
        np_imgs_ids = [
            news_promo.seo_image_id,
            news_promo.banner_id,
        ]
        gallery = news_promo.gallery
        news_promo.delete()
        gallery_imgs_ids = list(gallery.images.values_list("id", flat=True))
        gallery.delete()
        imgs_ids_for_delete = np_imgs_ids + gallery_imgs_ids
        self.image_service.bulk_delete(imgs_ids_for_delete)
        if promo:
            return MessageOutSchema(detail=_("Акція успішно видалена"))
        return MessageOutSchema(detail=_("Новина успішно видалена"))
