from src.cinemas.models import Hall, Cinema
from src.cinemas.schemas.hall import HallInSchema, HallUpdateSchema
from django.utils.translation import gettext as _
from src.cinemas.services.cinema import CinemaService
from src.core.schemas.base import MessageOutSchema
from src.core.errors import NotUniqueFieldExceptionError
from src.core.services.gallery import GalleryService
from src.core.services.images import ImageService
from injector import inject


class HallService:
    """
    A service class for managing hall.
    """

    @inject
    def __init__(self,
                 image_service: ImageService,
                 cinema_service: CinemaService,
                 gallery_service: GalleryService):
        self.cinema_service = cinema_service
        self.image_service = image_service
        self.gallery_service = gallery_service

    def create(self, schema: HallInSchema, cnm_slug: str) \
            -> MessageOutSchema:
        """
        Create hall.
        """
        cinema = self.cinema_service.get_by_slug(cnm_slug)
        self.check_number_unique(cinema=cinema, number=schema.number)
        bodies = [schema.banner, schema.seo_image]
        banner, seo_image = (self.image_service
                             .bulk_create(schemas=bodies))
        gallery = self.gallery_service.create(images=schema.gallery)
        Hall.objects.create(
            number=schema.number,
            description_uk=schema.description_uk,
            description_ru=schema.description_ru,
            banner=banner,
            tech=schema.tech.value,
            cinema=cinema,
            gallery=gallery,
            seo_title=schema.seo_title,
            seo_description=schema.seo_description,
            seo_image=seo_image,
        )
        return MessageOutSchema(detail=_('Зал успішно створений'))

    def update(self, hall_id: int, schema: HallUpdateSchema) \
            -> MessageOutSchema:
        """
        Update hall.
        """
        hall = Hall.objects.get_by_id(hall_id=hall_id)
        self.check_number_unique(cinema=hall.cinema,
                                 number=schema.number,
                                 hall=hall)
        self.image_service.update(schema.banner, hall.banner)
        self.image_service.update(schema.seo_image, hall.seo_image)

        self.gallery_service.update(schemas=schema.gallery,
                                    gallery=hall.gallery)
        expt_list = ['banner', 'seo_image', 'gallery']
        for attr, value in schema.dict().items():
            if attr not in expt_list and value is not None:
                setattr(hall, attr, value)
        hall.save()
        return MessageOutSchema(detail=_('Зал успішно оновлений'))

    @staticmethod
    def check_number_unique(cinema: Cinema, number: str,
                            hall: Hall = None) -> None:
        """
        Check that number of new hall is unique behind
        others number of halls in selected cinema.
        """
        halls = cinema.hall_set.filter(number=number)
        if halls and hall:
            halls = halls.exclude(id=hall.id)
        if halls.count():
            msg = _('Це поле повинно бути унікальним '
                    'по відношенню до конкретного кінотеатру. '
                    f'*{number}* - цей номер вже зайнятий. '
                    f'Для кінотеатру {cinema.name}'
                    )
            raise NotUniqueFieldExceptionError(message=msg,
                                               field='number')

    @staticmethod
    def get_by_id(hall_id: int) -> Hall:
        """
        Get hall by id.
        """
        hall = Hall.objects.get_by_id(hall_id=hall_id)

        return hall

    def get_all(self, cnm_slug: str) -> Hall:
        """
        Get all halls.
        :param cnm_slug: slug of parent cinema
        """
        cinema = self.cinema_service.get_by_slug(cnm_slug)
        hall = Hall.objects.filter(cinema=cinema)
        return hall

    def delete_by_id(self, hall_id: int) -> MessageOutSchema:
        """
        Delete hall.
        """
        hall = (Hall.objects
                .get_by_id(hall_id=hall_id))
        hall_imgs_ids = [hall.seo_image_id,
                         hall.banner_id, ]
        gallery = hall.gallery
        hall.delete()
        gallery_imgs_ids = list(gallery.images.values_list('id',
                                                           flat=True))
        gallery.delete()
        imgs_ids_for_delete = hall_imgs_ids + gallery_imgs_ids
        self.image_service.bulk_delete(imgs_ids_for_delete)
        return MessageOutSchema(detail=_('Зал успішно видалений'))
