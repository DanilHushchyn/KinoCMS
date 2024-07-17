from django.db.models import QuerySet
from django.http import HttpRequest
from src.core.errors import NotFoundExceptionError
from src.core.utils import make_slug
from src.pages.errors import PageUnableToDeleteExceptionError
from src.pages.models import Page
from src.pages.schemas.page import (PageInSchema,
                                    PageUpdateSchema)
from django.utils.translation import gettext as _

from src.core.schemas.base import MessageOutSchema
from src.core.services.core import CoreService
from src.core.services.gallery import GalleryService
from src.core.services.images import ImageService
from injector import inject


class PageService:
    """
    A service class for managing page.
    """

    @inject
    def __init__(self,
                 image_service: ImageService,
                 core_service: CoreService,
                 gallery_service: GalleryService):
        self.image_service = image_service
        self.gallery_service = gallery_service
        self.core_service = core_service

    def create(self, request: HttpRequest, schema: PageInSchema) \
            -> MessageOutSchema:
        """
        Create page.
        """
        self.core_service.check_field_unique(
            value=schema.name_uk,
            field_name='name_uk',
            model=Page)
        self.core_service.check_field_unique(
            value=schema.name_ru,
            field_name='name_ru',
            model=Page)
        bodies = [schema.banner, schema.seo_image]
        banner, seo_image = (self.image_service
                             .bulk_create(schemas=bodies))
        gallery = self.gallery_service.create(images=schema.gallery)

        Page.objects.create(
            name_uk=schema.name_uk,
            name_ru=schema.name_ru,
            slug=make_slug(value=schema.name_uk,
                           model=Page),
            content_uk=schema.content_uk,
            content_ru=schema.content_ru,
            banner=banner,
            active=schema.active,
            gallery=gallery,
            seo_title=schema.seo_title,
            seo_description=schema.seo_description,
            seo_image=seo_image,
        )
        return MessageOutSchema(detail=_('Сторінка успішно створена'))

    def update(self, request: HttpRequest, pg_slug: str,
               schema: PageUpdateSchema) \
            -> MessageOutSchema:
        """
        Update page.
        """
        page = Page.objects.get_by_slug(pg_slug=pg_slug)
        self.core_service.check_field_unique(
            value=schema.name_uk,
            field_name='name_uk',
            instance=page,
            model=Page)
        self.core_service.check_field_unique(
            value=schema.name_ru,
            field_name='name_ru',
            instance=page,
            model=Page)
        self.image_service.update(schema.banner, page.banner)
        self.image_service.update(schema.seo_image, page.seo_image)

        self.gallery_service.update(schemas=schema.gallery,
                                    gallery=page.gallery)
        expt_list = ['banner', 'seo_image', 'gallery']
        for attr, value in schema.dict().items():
            if attr not in expt_list and value is not None:
                setattr(page, attr, value)
        page.slug = make_slug(value=page.name_uk,
                              model=Page,
                              instance=page)
        page.save()
        return MessageOutSchema(detail=_('Сторінка успішно оновлена'))

    @staticmethod
    def get_by_slug(pg_slug: str) -> Page:
        """
        Get page by slug.
        """
        page = Page.objects.get_by_slug(pg_slug=pg_slug)
        return page

    @staticmethod
    def get_active_by_slug(pg_slug: str) -> Page:
        """
        Get page by slug.
        """
        page = Page.objects.get_by_slug(pg_slug=pg_slug)
        if page.active is False:
            msg = _('Не знайдено: немає збігів сторінок '
                    'на заданному запиті.')
            raise NotFoundExceptionError(message=msg, cls_model=Page)
        return page

    @staticmethod
    def get_all() -> QuerySet[Page]:
        """
        Get all pages.
        """

        pages = Page.objects.all()
        return pages

    @staticmethod
    def get_all_active() -> QuerySet[Page]:
        """
        Get all active pages.
        """

        pages = Page.objects.filter(active=True)
        return pages

    def delete_by_slug(self, pg_slug: str) -> MessageOutSchema:
        """
        Delete page.
        """
        page = (Page.objects
                .get_by_slug(pg_slug=pg_slug))
        if not page.can_delete:
            msg = _('Цю сторінку заборонено видаляти')
            raise PageUnableToDeleteExceptionError(message=msg)
        pg_imgs_ids = [page.seo_image_id,
                       page.banner_id, ]
        gallery = page.gallery
        page.delete()
        gallery_imgs_ids = list(gallery.images.values_list('id', flat=True))
        gallery.delete()
        imgs_ids_for_delete = pg_imgs_ids + gallery_imgs_ids
        self.image_service.bulk_delete(imgs_ids_for_delete)
        return MessageOutSchema(detail=_('Сторінка успішно видалена'))
