from django.db.models import Q
from ninja.errors import HttpError

from src.cinemas.models import Cinema
from src.cinemas.schemas.cinema import CinemaInSchema, CinemaUpdateSchema
from django.utils.translation import gettext as _
from pytils.translit import slugify

from src.core.schemas.base import MessageOutSchema
from src.core.services.gallery import GalleryService
from src.core.services.images import ImageService
from injector import inject


class CinemaService:
    """
    A service class for managing cinema.
    """

    @inject
    def __init__(self, image_service: ImageService,
                 gallery_service: GalleryService):
        self.image_service = image_service
        self.gallery_service = gallery_service

    def create(self, schema: CinemaInSchema) -> Cinema:
        """
        Create cinema.
        """
        self.check_cnm_name_unique(schema.name_uk)
        self.check_cnm_name_unique(schema.name_ru)
        bodies = [schema.banner, schema.logo, schema.seo_image]
        banner, logo, seo_image = (self.image_service
                                   .bulk_create(schemas=bodies))
        gallery = self.gallery_service.create(images=schema.gallery)

        cinema = Cinema.objects.create(
            name_uk=schema.name_uk,
            name_ru=schema.name_ru,
            slug=slugify(schema.name_uk),
            description_uk=schema.description_uk,
            description_ru=schema.description_ru,
            banner=banner,
            logo=logo,
            terms_uk=schema.terms_uk,
            terms_ru=schema.terms_ru,
            address=schema.address,
            coordinate=schema.coordinate,
            gallery=gallery,
            seo_title=schema.seo_title,
            seo_description=schema.seo_description,
            seo_image=seo_image,
        )
        return cinema

    def update(self, cnm_slug: str, schema: CinemaUpdateSchema) \
            -> MessageOutSchema:
        """
        Update cinema.
        """
        cinema = Cinema.objects.get_by_slug(cnm_slug=cnm_slug)
        self.check_cnm_name_unique(schema.name_uk, cinema)
        self.check_cnm_name_unique(schema.name_ru, cinema)
        self.image_service.update(schema.banner, cinema.banner)
        self.image_service.update(schema.logo, cinema.logo)
        self.image_service.update(schema.seo_image, cinema.seo_image)

        self.gallery_service.update(schemas=schema.gallery,
                                    gallery=cinema.gallery)
        expt_list = ['banner', 'logo', 'seo_image', 'gallery']
        for attr, value in schema.dict().items():
            if attr not in expt_list and value is not None:
                setattr(cinema, attr, value)
        cinema.slug = slugify(cinema.name_uk)
        cinema.save()
        return MessageOutSchema(detail=_('Кінотеатр успішно оновлений'))

    @staticmethod
    def get_by_slug(cnm_slug: str) -> Cinema:
        """
        Get cinema by slug.
        """
        cinema = Cinema.objects.get_by_slug(cnm_slug=cnm_slug)
        return cinema

    @staticmethod
    def get_all() -> Cinema:
        """
        Get all cinemas.
        """
        cinema = Cinema.objects.all()
        return cinema

    @staticmethod
    def check_cnm_name_unique(value: str, cinema_obj: Cinema = None) -> bool:
        """
        Check name for cinema unique.
        """
        if value is not None:
            cinemas = Cinema.objects.filter(Q(name_uk=value) |
                                            Q(name_ru=value))
            if cinemas and cinema_obj:
                cinemas = cinemas.exclude(id=cinema_obj.id)
            if cinemas.count():
                msg = _('Поле name повинно бути унікальним. '
                        'Ця назва вже зайнята')
                raise HttpError(409, msg)
            else:
                return True

    def delete_by_slug(self, cnm_slug: str) -> MessageOutSchema:
        """
        Delete cinema.
        """
        cinema = (Cinema.objects
                  .get_by_slug(cnm_slug=cnm_slug))
        cnm_imgs_ids = [cinema.seo_image_id,
                        cinema.banner_id,
                        cinema.logo_id]
        gallery = cinema.gallery
        cinema.delete()
        gallery_imgs_ids = list(gallery.images.values_list('id', flat=True))
        gallery.delete()
        imgs_ids_for_delete = cnm_imgs_ids + gallery_imgs_ids
        self.image_service.bulk_delete(imgs_ids_for_delete)
        return MessageOutSchema(detail=_('Кінотеатр успішно видалений'))
