from ninja import ModelSchema
import ninja_schema
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
        # request = self.context.get('request')
        return str(obj.image.url)

    class Meta:
        model = Image
        fields = '__all__'
