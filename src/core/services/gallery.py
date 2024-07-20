from injector import inject

from src.core.errors import NotFoundExceptionError
from src.core.models import Gallery
from src.core.models import Image
from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import ImageInSchema
from src.core.services.images import ImageService


class GalleryService:
    """A service class for managing gallery."""

    @inject
    def __init__(self, image_service: ImageService):
        self.image_service = image_service

    def create(self, images: list[ImageInSchema]) -> Gallery:
        """Create gallery."""
        gallery = Gallery.objects.create()
        if images:
            list_of_images = self.image_service.bulk_create(schemas=images)
            gallery.images.set(list_of_images)
        return gallery

    def update(self, schemas: list[GalleryItemSchema], gallery: Gallery) -> None:
        """Update gallery."""
        if schemas:
            for schema in schemas:
                if schema.id:
                    img = self.image_service.get_image(schema.id)
                    self.image_matches_gallery(gallery, schema.id)
                    if schema.delete:
                        self.image_service.delete(img)
                    else:
                        self.image_service.update(schema, img)
                elif not schema.delete:
                    image_obj = self.image_service.create(schema)
                    gallery.images.add(image_obj)
                    gallery.save()

    @staticmethod
    def get_by_id(gallery_id: int) -> Gallery:
        """Get gallery by id."""
        gallery = Gallery.objects.get_by_id(gallery_id=gallery_id)
        return gallery.images.all()

    @staticmethod
    def image_matches_gallery(gallery: Gallery, img_id: int) -> None:
        """Get gallery by id."""
        ids = gallery.images.values_list("id", flat=True)
        if img_id not in ids:
            msg = f"Дане зображення id({img_id}) " "не належить до галереї кінотеатру"
            raise NotFoundExceptionError(message=msg, cls_model=Image)
