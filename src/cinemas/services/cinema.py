from src.cinemas.models import Cinema
from src.cinemas.schemas.cinema import CinemaInSchema
from django.utils.translation import gettext as _
from pytils.translit import slugify

from src.core.schemas.base import MessageOutSchema


class CinemaService:
    """
    A service class for managing cinema.
    """

    @staticmethod
    def create(body: CinemaInSchema) -> Cinema:
        """
        Create cinema.
        """
        cinema = Cinema.objects.create(
            name_uk=body.name_uk,
            name_ru=body.name_ru,
            slug=slugify(body.name_uk),
            description_uk=body.description_uk,
            description_ru=body.description_ru,
            banner_id=body.banner,
            card_img_id=body.card_img,
            logo_id=body.logo,
            address=body.address,
            coordinate=body.coordinate,
            gallery_id=body.gallery,
            seo_title=body.seo_title,
            seo_description=body.seo_description,
            seo_image_id=body.seo_image,
        )
        return cinema

    @staticmethod
    def get_by_id(cinema_id: int) -> Cinema:
        """
        Create cinema.
        """
        cinema = Cinema.objects.get_by_id(cinema_id=cinema_id)
        return cinema

    @staticmethod
    def delete_by_id(cinema_id: int) -> MessageOutSchema:
        """
        Delete cinema.
        """
        cinema = Cinema.objects.get_by_id(cinema_id=cinema_id)
        cinema.delete()
        return MessageOutSchema(detail=_('Кінотеатр успішно видалений'))

