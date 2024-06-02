from django.db.models import QuerySet
from injector import inject

from src.core.schemas.base import MessageOutSchema
from src.core.services.core import CoreService
from src.core.services.gallery import GalleryService
from src.core.services.images import ImageService
from src.movies.schemas import *
from django.utils.translation import gettext as _
from pytils.translit import slugify


class MovieService:
    """
    A service class for managing movies.
    """

    @inject
    def __init__(self, image_service: ImageService,
                 core_service: CoreService,
                 gall_service: GalleryService):

        self.core_service = core_service
        self.image_service = image_service
        self.gall_service = gall_service

    def create(self, schema: MovieInSchema) -> MessageOutSchema:
        """
        Create Movie.
        """
        self.core_service.check_name_unique(value=schema.name_uk,
                                            model=Movie)
        self.core_service.check_name_unique(value=schema.name_ru,
                                            model=Movie)
        bodies = [schema.card_img, schema.seo_image]
        card_img, seo_image = (self.image_service
                               .bulk_create(schemas=bodies))
        gallery = self.gall_service.create(images=schema.gallery)

        Movie.objects.create(
            name_uk=schema.name_uk,
            name_ru=schema.name_ru,
            slug=slugify(schema.name_uk),
            description_uk=schema.description_uk,
            description_ru=schema.description_ru,
            gallery=gallery,
            card_img=card_img,
            countries=schema.countries,
            seo_title=schema.seo_title,
            seo_description=schema.seo_description,
            seo_image=seo_image,
        )
        return MessageOutSchema(detail=_('Фільм успішно створений'))

    def update(self, mv_slug: str, schema: MovieUpdateSchema) \
            -> MessageOutSchema:
        """
        Update Movie.
        """
        movie = Movie.objects.get_by_slug(mv_slug=mv_slug)
        self.core_service.check_name_unique(value=schema.name_uk,
                                            instance=movie,
                                            model=Movie)
        self.core_service.check_name_unique(value=schema.name_ru,
                                            instance=movie,
                                            model=Movie)
        self.image_service.update(schema.banner, movie.banner)
        self.image_service.update(schema.logo, movie.card_img)
        self.image_service.update(schema.seo_image, movie.seo_image)

        self.gall_service.update(schemas=schema.gallery,
                                 gallery=Movie.gallery)
        expt_list = ['banner', 'card_img', 'seo_image', 'gallery']
        for attr, value in schema.dict().items():
            if attr not in expt_list and value is not None:
                setattr(movie, attr, value)
        movie.slug = slugify(movie.name_uk)
        movie.save()
        return MessageOutSchema(detail=_('Кінотеатр успішно оновлений'))

    #
    @staticmethod
    def get_by_slug(mv_slug: str) -> Movie:
        """
        Get movie by slug.
        """
        movie = Movie.objects.get_by_slug(mv_slug=mv_slug)
        return movie

    @staticmethod
    def get_all() -> QuerySet:
        """
        Get all movies.
        """
        movie = Movie.objects.all()
        return movie

    def delete_by_slug(self, mv_slug: str) -> MessageOutSchema:
        """
        Delete movie by slug.
        """
        movie = (Movie.objects
                 .get_by_slug(mv_slug=mv_slug))
        movie_imgs_ids = [movie.seo_image_id,
                          movie.card_img_id]
        gall = movie.gallery
        movie.delete()
        gall_imgs_ids = gall.images.values_list('id', flat=True)
        gall.delete()
        gall_imgs_ids = list(gall_imgs_ids)
        imgs_ids_for_delete = movie_imgs_ids + gall_imgs_ids
        self.image_service.bulk_delete(imgs_ids_for_delete)
        return MessageOutSchema(detail=_('Фільм успішно видалений'))
