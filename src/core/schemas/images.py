from ninja import ModelSchema
import ninja_schema

from config.settings.settings import ABSOLUTE_URL
from src.core.models import Image


class ImageInSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for uploading image to server side.
    """

    class Config:
        model = Image
        include = ['alt']


class ImageOutSchema(ModelSchema):
    """
    Pydantic schema for return image to client side.
    """
    image: str

    @staticmethod
    def resolve_image(obj: Image):
        return ABSOLUTE_URL+str(obj.image.url)

    class Meta:
        model = Image
        fields = '__all__'
