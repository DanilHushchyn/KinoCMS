from src.cinemas.models import Cinema
from src.cinemas.schemas.cinema import CinemaInSchema
from django.utils.translation import gettext as _
from pytils.translit import slugify

from src.core.schemas.base import MessageOutSchema
from src.core.services.gallery import GalleryService
from src.core.services.images import ImageService
from injector import Binder, singleton, inject, provider


class CinemaService:
    """
    A service class for managing cinema.
    """

    # def configure(self, binder: Binder) -> Binder:
    #     binder.bind(ImageService, to=ImageServiceImpl, scope=singleton)

    @inject
    def __init__(self, image_service: ImageService,
                 gallery_service: GalleryService):
        self.image_service = image_service
        self.gallery_service = gallery_service

    def create(self, body: CinemaInSchema) -> Cinema:
        """
        Create cinema.
        """
        banner = self.image_service.create(body=body.banner)
        logo = self.image_service.create(body=body.logo)
        seo_image = self.image_service.create(body=body.seo_image)
        gallery = self.gallery_service.create(images=body.gallery)

        cinema = Cinema.objects.create(
            name_uk=body.name_uk,
            name_ru=body.name_ru,
            slug=slugify(body.name_uk),
            description_uk=body.description_uk,
            description_ru=body.description_ru,
            banner=banner,
            logo=logo,
            address=body.address,
            coordinate=body.coordinate,
            gallery=gallery,
            seo_title=body.seo_title,
            seo_description=body.seo_description,
            seo_image=seo_image,
        )
        return cinema

    @staticmethod
    def get_by_slug(cnm_slug: str) -> Cinema:
        """
        Create cinema.
        """
        cinema = Cinema.objects.get_by_slug(cnm_slug=cnm_slug)
        return cinema

    @staticmethod
    def delete_by_slug(cnm_slug: str) -> MessageOutSchema:
        """
        Delete cinema.
        """
        cinema = Cinema.objects.get_by_slug(cnm_slug=cnm_slug)
        cinema.banner.delete() if cinema.banner else ...
        cinema.seo_image.delete() if cinema.seo_image else ...
        cinema.logo.delete() if cinema.logo else ...
        for img in cinema.gallery.images.all():
            img.delete() if img else ...
        cinema.gallery.delete() if cinema.gallery else ...
        cinema.delete()
        return MessageOutSchema(detail=_('Кінотеатр успішно видалений'))
