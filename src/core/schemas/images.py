from django.forms import Form
from ninja import ModelSchema, File, UploadedFile, Schema
import ninja_schema
from pydantic import FileUrl, FilePath

from src.core.models import Image


# class ImageInSchema(Schema):
#     """
#     Pydantic schema for uploading image to server side.
#     """
#     image: File[UploadedFile]
#     alt: str

    # class Meta:
    #     model = Image
    #     fields = ['alt', 'image']

    # class Config:
    #     model = Image
    #     include = ['alt', 'image']


class ImageOutSchema(ModelSchema):
    """
    Pydantic schema for return image to client side.
    """

    class Meta:
        model = Image
        fields = '__all__'
