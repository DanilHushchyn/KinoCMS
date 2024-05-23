from src.core.models import Image, Gallery
from src.core.schemas.gallery import GalleryInSchema


class GalleryService:
    """
    A service class for managing gallery.
    """

    @staticmethod
    def create(body: GalleryInSchema) -> Gallery:
        """
        Create gallery.
        """
        gallery = Gallery.objects.create()
        gallery.images.set(body.images)
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
