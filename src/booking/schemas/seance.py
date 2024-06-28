from typing import List, Any
import ninja_schema
from ninja.errors import HttpError
from phonenumber_field.validators import validate_international_phonenumber
from pydantic.fields import Field
from src.booking.models import Seance
from ninja import ModelSchema
from django.utils.translation import gettext as _
from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import ImageOutSchema, ImageInSchema, ImageUpdateSchema
from pydantic import Json
from django.core.exceptions import ValidationError


class SeanceCardOutSchema(ModelSchema):
    """
    Pydantic schema for showing séance card.
    """
    card_img: ImageOutSchema

    @staticmethod
    def resolve_card_img(obj: Seance):
        return obj.movie.card_img

    class Meta:
        model = Seance
        fields = ['price',
                  'date',
                  'id', ]


# class SeanceOutSchema(ModelSchema):
#     """
#     Pydantic schema for showing seance full data.
#     """
#     banner: ImageOutSchema
#     logo: ImageOutSchema
#     seo_image: ImageOutSchema
#
#     @staticmethod
#     def resolve_phone_1(obj: Seance):
#         return str(obj.phone_1)
#
#     @staticmethod
#     def resolve_phone_2(obj: Seance):
#         return str(obj.phone_2)
#
#     class Meta:
#         model = Seance
#         exclude = ['id', 'name', 'description', 'address',
#                    'terms', 'slug', 'date_created']
