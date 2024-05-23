from ninja.errors import HttpError
from ninja import File
from src.core.models import Image
from src.core.schemas.base import MessageOutSchema
from django.utils.translation import gettext as _
import loguru


class ImageService:
    """
    A service class for managing images.
    """

    def __init__(self):
        self.image_types = ['image/jpeg', 'image/png', 'image/svg',
                            'image/svg+xml', 'image/webp', 'image/jpeg']

    def check_image(self, image: File):
        if image.content_type not in self.image_types:
            msg = _(f'Дозволено відправляти тільки {self.image_types}')
            raise HttpError(403, msg)
        if image.size > 1_000_000:
            msg = _('Максимально дозволений розмір файлу 1MB')
            raise HttpError(403, msg)

    def upload_image(self, alt: str, image: File, img_id: int) -> Image:
        """
        Upload image to server side for some entity.
        """

        self.check_image(image)
        if img_id is not None:
            obj = Image.objects.get_by_id(img_id=img_id)
            obj.image = image
            obj.alt = alt
            obj.save()
        else:
            obj = Image.objects.create(image=image, alt=alt)
        return obj

    @staticmethod
    def delete_image(img_id: int) -> MessageOutSchema:
        """
         delete image by id.
        """
        image = Image.objects.get_by_id(img_id=img_id)
        image.delete()

        return MessageOutSchema(detail=_('Картинка успішно видалена'))

    @staticmethod
    def get_image(img_id: int) -> Image:
        """
         get image by id.
        """
        obj = Image.objects.get_by_id(img_id=img_id)

        return obj
