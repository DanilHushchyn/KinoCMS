import binascii
import io
from base64 import b64decode

from django.core.files.base import ContentFile
from ninja.errors import HttpError
import src.core.models as im
from src.core.schemas.base import MessageOutSchema
from django.utils.translation import gettext as _
from PIL import Image
from src.core.schemas.images import ImageInSchema


class ImageService:
    """
    A service class for managing images.
    """

    def __init__(self):
        self.image_types = ['jpeg', 'jpg', 'png',
                            'svg', 'webp', ]

    @staticmethod
    def check_image(image_base64: str, filename: str):
        name, extension = filename.split('.')
        try:
            head, image_base64 = image_base64.split(',')
            img_obj = b64decode(image_base64, validate=True)
            if extension != 'svg':
                img = Image.open(io.BytesIO(img_obj))
                img.verify()
        except binascii.Error as e:
            msg = _('Невірний формат base64 був відправлений')
            raise HttpError(403, msg)
        except Exception as e:
            raise HttpError(403, _('Файл пошкоджений'))
        image_field = ContentFile(img_obj, filename)
        if image_field.size > 1_000_000:
            msg = _('Максимально дозволений розмір файлу 1MB')
            raise HttpError(403, msg)
        return image_field

    def create(self, body: ImageInSchema) \
            -> Image:
        """
        Create image to server side for some entity.
        json format

        """
        filename = body.filename
        image_base64 = body.image
        alt_text = body.alt
        image_field = self.check_image(image_base64=image_base64,
                                       filename=filename)
        name, extension = filename.split('.')
        if not alt_text:
            alt_text = name
        obj = im.Image.objects.create(image=image_field, alt=alt_text)
        return obj

    @staticmethod
    def delete_image(img_id: int) -> MessageOutSchema:
        """
         delete image by id.
        """
        image = im.Image.objects.get_by_id(img_id=img_id)
        image.delete()

        return MessageOutSchema(detail=_('Картинка успішно видалена'))

    @staticmethod
    def get_image(img_id: int) -> Image:
        """
         get image by id.
        """
        obj = im.Image.objects.get_by_id(img_id=img_id)

        return obj
