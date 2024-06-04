from pydantic.functional_validators import field_validator

from src.core.models import Seo
from src.core.utils import validate_max_length
from ninja import Schema


class SeoInSchema:
    """
    Pydantic schema for validation seo data.
    """
    seo_title: str
    seo_description: str

    @field_validator('seo_title')
    def clean_seo_description_max_length(cls, seo_title: str) \
            -> str:
        validate_max_length(available=60,
                            current=len(seo_title),
                            field_name='seo_title')
        return seo_title

    @field_validator('seo_description')
    def clean_seo_description_max_length(cls, seo_description: str) \
            -> str:
        validate_max_length(available=160,
                            current=len(seo_description),
                            field_name='seo_description')
        return seo_description
