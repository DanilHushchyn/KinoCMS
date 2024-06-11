import re
from typing import List

import ninja_schema
from ninja.errors import HttpError

from ninja import ModelSchema
from django.utils.translation import gettext as _
from pydantic.functional_validators import field_validator
from matplotlib.colors import is_color_like
from src.core.schemas.images import ImageOutSchema, ImageInSchema, ImageUpdateSchema
from src.core.utils import validate_capitalized
from src.pages.models import TopSlider, TopSliderItem, BottomSliderItem, BottomSlider, ETEndBBanner


class TopSliderItemUpdateSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for updating or creating TopSliderItem.
    """
    delete: bool
    image: ImageUpdateSchema = None

    @ninja_schema.model_validator('text_uk', 'text_ru')
    def clean_capitalize(cls, value) -> str:
        msg = _('Недійсне значення (не написане великими літерами). '
                'З великих літер повиннен починатися text')
        validate_capitalized(value, msg)
        return value

    class Config:
        model = TopSliderItem
        include = [
            'id',
            'url',
            'text_uk',
            'text_ru',
            'image',
        ]
        optional = ['id', ]


class TopSliderUpdateSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for updating TopSlider.
    """

    items: List[TopSliderItemUpdateSchema] = None

    @ninja_schema.model_validator('speed')
    def clean_speed(cls, speed) -> int:
        return speed.value

    class Config:
        model = TopSlider
        include = [
            'speed',
            'active',
        ]


class BottomSliderItemUpdateSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for updating or creating BottomSliderItem.
    """
    delete: bool
    image: ImageUpdateSchema = None

    class Config:
        model = BottomSliderItem
        include = [
            'id',
            'url',
            'image',
        ]
        optional = ['id', ]


class BottomSliderUpdateSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for updating BottomSlider.
    """

    items: List[BottomSliderItemUpdateSchema] = None

    @ninja_schema.model_validator('speed')
    def clean_speed(cls, speed) -> int:
        return speed.value

    class Config:
        model = BottomSlider
        include = [
            'speed',
            'active',
        ]


class TopSliderItemOutSchema(ModelSchema):
    """
    Pydantic schema for getting Top slider items.
    """
    image: ImageOutSchema

    class Meta:
        model = TopSliderItem
        fields = [
            'id',
            'url',
            'text_uk',
            'text_ru',
            'image',
        ]


class TopSliderOutSchema(ModelSchema):
    """
    Pydantic schema for getting Top slider.
    """

    items: List[TopSliderItemOutSchema]

    class Meta:
        model = TopSlider
        fields = [
            'speed',
            'active',
        ]


class BottomSliderItemOutSchema(ModelSchema):
    """
    Pydantic schema for getting Bottom slider items.
    """
    image: ImageOutSchema

    class Meta:
        model = BottomSliderItem
        fields = [
            'id',
            'url',
            'image',
        ]


class BottomSliderOutSchema(ModelSchema):
    """
    Pydantic schema for getting Bottom slider.
    """

    items: List[BottomSliderItemOutSchema]

    class Meta:
        model = BottomSlider
        fields = [
            'speed',
            'active',
        ]


class ETEndBBannerUpdateSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for updating ETEndBBanner.
    """

    image: ImageUpdateSchema = None

    @ninja_schema.model_validator('color')
    def clean_color(cls, color) -> str:
        if is_color_like(color):
            return color
        else:
            msg = _('Невірний формат кольору було введено')
            raise HttpError(403, msg)

    class Config:
        model = ETEndBBanner
        include = [
            'color',
            'use_img',
            'image',
        ]
        optional = ("use_img",)


class ETEndBBannerOutSchema(ModelSchema):
    """
    Pydantic schema for getting ETEndBBanner.
    """

    image: ImageOutSchema

    class Meta:
        model = ETEndBBanner
        fields = [
            'color',
            'use_img',
            'image',
        ]
