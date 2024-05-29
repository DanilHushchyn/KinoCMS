import binascii
import io
import shutil
from base64 import b64decode
from pathlib import Path
from typing import List

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
import src.core.models as im
from src.core.schemas.base import MessageOutSchema
from django.utils.translation import gettext as _
from PIL import Image
from src.core.schemas.images import ImageInSchema, ImageUpdateSchema


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

    def update(self, body: ImageUpdateSchema, parent: object) \
            -> Image:
        """
        Update image in json format
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

    def update(self, img: ImageUpdateSchema, related_img: im.Image) \
            -> None:
        """
        Update image in json format
        """
        if img:
            image_obj = get_object_or_404(Image, pk=img.id)
            if image_obj != related_img:
                msg = f'Incorrect id {img.id} for image'
                raise HttpError(409, msg)
            filename = img.filename
            image_base64 = img.image
            alt_text = img.alt
            if filename and image_base64:
                image_field = self.check_image(image_base64=image_base64,
                                               filename=filename)
                image_obj.image = image_field
            if alt_text:
                image_obj.alt = alt_text
            image_obj.save()

    def bulk_create(self, bodies: List[ImageInSchema]) -> im.Image:
        """
        Create image to server side for some entity.
        json format

        """
        images = []
        for body in bodies:
            filename = body.filename
            image_base64 = body.image
            alt_text = body.alt
            image_field = self.check_image(image_base64=image_base64,
                                           filename=filename)
            name, extension = filename.split('.')
            if not alt_text:
                alt_text = name
            images.append(im.Image(image=image_field, alt=alt_text))
        list_of_images = im.Image.objects.bulk_create(images)
        return list_of_images

    @staticmethod
    def delete_image(instance: im.Image) -> None:
        """
         delete image.
        """
        if instance:
            name = instance.image.name
            dir_path = Path(name).stem
            dir_to_rem = Path(f"media/CACHE/images/Image/{dir_path}")
            if dir_to_rem.is_dir():
                shutil.rmtree(dir_to_rem)
            instance.delete()

    @staticmethod
    def get_image(img_id: int) -> Image:
        """
         get image by id.
        """
        obj = im.Image.objects.get_by_id(img_id=img_id)

        return obj
