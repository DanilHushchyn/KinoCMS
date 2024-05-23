from typing import List

import ninja_schema

from src.core.models import Gallery, Image
from ninja import ModelSchema

from src.core.schemas.images import ImageOutSchema


class GalleryInSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for uploading image to server side.
    """

    @ninja_schema.model_validator('images')
    def clean_images(cls, images) -> list:
        Image.objects.check_of_ids(images)
        return images

    class Config:
        model = Gallery
        include = ['images']


class GalleryMinOutSchema(ModelSchema):
    """
    Pydantic schema for return image to client side.
    """

    class Meta:
        model = Gallery
        fields = '__all__'


class GalleryMaxOutSchema(ModelSchema):
    """
    Pydantic schema for return image to client side.
    """
    images: List[ImageOutSchema]

    class Meta:
        model = Gallery
        fields = '__all__'
