"""Service for working with images"""

import binascii
import io
import shutil
from base64 import b64decode
from pathlib import Path

from django.core.files.base import ContentFile
from django.utils.translation import gettext as _
from PIL import Image

import src.core.models as im
from src.core.errors import UnprocessableEntityExceptionError
from src.core.schemas.images import ImageInSchema
from src.core.schemas.images import ImageUpdateSchema


class ImageService:
    """A service class for managing images."""

    def __init__(self):
        self.image_types = [
            "jpeg",
            "jpg",
            "png",
            "svg",
            "webp",
        ]

    @staticmethod
    def check_image(image_base64: str, filename: str) -> ContentFile:
        """Check base64 image is valid
        :param image_base64: image encoded in base64
        :param filename: metadata for image
        :return: image object
        """
        try:
            name, extension = filename.split(".")
            img_obj = b64decode(image_base64, validate=True)
            if extension != "svg":
                img = Image.open(io.BytesIO(img_obj))
                img.verify()
            image_field = ContentFile(img_obj, filename)
        except binascii.Error:
            msg = _("Невірний формат base64 був відправлений")
            raise UnprocessableEntityExceptionError(message=msg)
        except Exception:
            msg = _("Файл пошкоджений")
            raise UnprocessableEntityExceptionError(message=msg)
        if image_field.size > 1_000_000:
            msg = _("Максимально дозволений розмір файлу 1MB")
            raise UnprocessableEntityExceptionError(message=msg)
        return image_field

    def create(self, schema: ImageInSchema) -> Image:
        """Create image to server side for some entity.
        json format
        """
        filename = schema.filename
        image_base64 = schema.image
        alt_text = schema.alt
        image_field = self.check_image(image_base64=image_base64, filename=filename)
        name, extension = filename.split(".")
        if not alt_text:
            alt_text = name
        obj = im.Image.objects.create(image=image_field, alt=alt_text)
        return obj

    def update(self, schema: ImageUpdateSchema, image_obj: im.Image) -> None:
        """Update image in json format"""
        if schema:
            filename = schema.filename
            image_base64 = schema.image
            if filename and image_base64:
                name, extension = filename.split(".")
                image_field = self.check_image(
                    image_base64=image_base64, filename=filename
                )
                self.clear_imagekit_cache(image_obj)
                image_obj.image = image_field
                image_obj.alt = name
            if schema.alt:
                image_obj.alt = schema.alt
            image_obj.save()

    def bulk_create(self, schemas: list[ImageInSchema]) -> im.Image:
        """Create image to server side for some entity.
        json format

        """
        images = []
        for schema in schemas:
            filename = schema.filename
            image_base64 = schema.image
            alt_text = schema.alt
            image_field = self.check_image(image_base64=image_base64, filename=filename)
            name, extension = filename.split(".")
            if not alt_text:
                alt_text = name
            images.append(im.Image(image=image_field, alt=alt_text))
        list_of_images = im.Image.objects.bulk_create(images)
        return list_of_images

    def delete(self, image_obj: im.Image) -> None:
        """Delete image."""
        if image_obj:
            self.clear_imagekit_cache(image_obj)
            image_obj.delete()

    def bulk_delete(self, image_ids: list[int]) -> None:
        """Delete multiple images."""
        images = im.Image.objects.filter(id__in=image_ids)
        for img in images:
            self.clear_imagekit_cache(img)
        images.delete()

    @staticmethod
    def get_image(img_id: int) -> Image:
        """Get image by id."""
        obj = im.Image.objects.get_by_id(img_id=img_id)

        return obj

    @staticmethod
    def clear_imagekit_cache(image_obj: im.Image) -> Image:
        """Clear webp image format which generates
        Imagekit library for each image in system.
        """
        name = image_obj.image.name
        dir_path = Path(name).stem
        dir_to_rem = Path(f"media/CACHE/images/Image/{dir_path}")
        if dir_to_rem.is_dir():
            shutil.rmtree(dir_to_rem)
