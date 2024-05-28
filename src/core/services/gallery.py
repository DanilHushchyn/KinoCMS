from typing import List

from src.core.models import Gallery
from src.core.schemas.gallery import GalleryInSchema
from src.core.schemas.images import ImageInSchema
from src.core.services.images import ImageService
from injector import Binder, singleton, inject, provider


class GalleryService:
    """
    A service class for managing gallery.
    """

    @inject
    def __init__(self, image_service: ImageService):
        self.image_service = image_service

    def create(self, images: List[ImageInSchema]) -> Gallery:
        """
        Create gallery.
        """
        gallery = Gallery.objects.create()
        for img in images:
            result = self.image_service.create(body=img)
            gallery.images.add(result)
        return gallery

    @staticmethod
    def update(body: GalleryInSchema, gallery_id: int) -> Gallery:
        """
        Update gallery.
        """
        gallery = Gallery.objects.get_by_id(gallery_id=gallery_id)
        gallery.images.clear()
        gallery.images.set(body.images)
        return gallery

    @staticmethod
    def get_by_id(gallery_id: int) -> Gallery:
        """
        Get gallery by id.
        """
        gallery = Gallery.objects.get_by_id(gallery_id=gallery_id)
        return gallery
