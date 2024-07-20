import ninja_schema
from django.utils.translation import gettext as _
from ninja import ModelSchema
from pydantic.fields import Field

from src.cinemas.models import Hall
from src.core.errors import NotFoundExceptionError
from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import ImageInSchema
from src.core.schemas.images import ImageOutSchema
from src.core.schemas.images import ImageUpdateSchema
from src.movies.models import Tech
from src.movies.schemas import TechOutSchema


class HallInSchema(ninja_schema.ModelSchema):
    """Pydantic schema for creating halls to server side."""

    banner: ImageInSchema
    seo_image: ImageInSchema
    gallery: list[ImageInSchema] = None

    description_uk: str = Field(max_length=2000)
    description_ru: str = Field(max_length=2000)

    @ninja_schema.model_validator("tech")
    def clean_tech(cls, tech_id: int) -> Tech:
        try:
            tech = Tech.objects.get(id=tech_id)
        except Tech.DoesNotExist:
            msg = _(
                "У заданому переліку технологій є "
                "id {tech_id} які не присутні у базі"
            ).format(tech_id=tech_id)
            raise NotFoundExceptionError(message=msg, cls_model=Tech, field="tech")
        return tech

    class Config:
        model = Hall
        include = [
            "number",
            "description_uk",
            "description_ru",
            "gallery",
            "banner",
            "tech",
            "seo_title",
            "seo_image",
            "seo_description",
        ]
        optional = [
            "gallery",
        ]


class HallCardOutSchema(ModelSchema):
    """Pydantic schema for showing hall card."""

    class Meta:
        model = Hall
        fields = [
            "number",
            "date_created",
            "id",
        ]


class HallOutSchema(ModelSchema):
    """Pydantic schema for showing hall full data."""

    banner: ImageOutSchema
    seo_image: ImageOutSchema
    tech: TechOutSchema

    class Meta:
        model = Hall
        fields = [
            "number",
            "description_uk",
            "description_ru",
            "gallery",
            "banner",
            "id",
            "tech",
            "seo_title",
            "seo_image",
            "seo_description",
        ]


class HallClientOutSchema(ModelSchema):
    """Pydantic schema for showing hall full data in the client site."""

    banner: ImageOutSchema
    seo_image: ImageOutSchema
    tech: TechOutSchema

    class Meta:
        model = Hall
        fields = [
            "number",
            "description",
            "gallery",
            "banner",
            "id",
            "seo_title",
            "seo_image",
            "seo_description",
        ]


class HallSchemaOutSchema(ModelSchema):
    """Pydantic schema for showing hall full data in the client site."""

    class Meta:
        model = Hall
        fields = ["layout"]


class HallUpdateSchema(ninja_schema.ModelSchema):
    """Pydantic schema for updating hall."""

    banner: ImageUpdateSchema = None
    seo_image: ImageUpdateSchema = None
    gallery: list[GalleryItemSchema] = None

    class Config:
        model = Hall
        include = [
            "number",
            "description_uk",
            "description_ru",
            "gallery",
            "banner",
            "seo_title",
            "seo_image",
            "seo_description",
        ]
        optional = "__all__"
