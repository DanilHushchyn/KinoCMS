from ninja.errors import HttpError
from ninja import File, Form
from ninja.files import UploadedFile
from src.core.models import Image
from src.core.schemas.base import MessageOutSchema
from src.core.schemas.images import ImageOutSchema
from django.utils.translation import gettext as _


class ImageService:
    """
    A service class for mailing.
    """

    @staticmethod
    def upload_image(alt: str, image) -> ImageOutSchema:
        """
        Upload image to server side for some entity.
        """
        # if body.image.content_type  []:
        #     msg = _('Дозволено відправляти тільки html')
        #     raise HttpError(403, msg)
        if image.size > 1_000_000:
            msg = _('Максимально дозволений розмір файлу 1MB')
            raise HttpError(403, msg)
        image = Image.objects.create(image=image, alt=alt)

        return image
