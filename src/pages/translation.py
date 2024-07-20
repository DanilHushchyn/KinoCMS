"""Module for translating essenses from app pages"""

from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import register

from src.pages.models import NewsPromo
from src.pages.models import Page
from src.pages.models import Tag
from src.pages.models import TopSliderItem


@register(TopSliderItem)
class TopSliderItemTranslationOptions(TranslationOptions):
    """Translate fields from model TopSliderItem"""

    fields = ("text",)
    required_languages = ("uk", "ru")


@register(NewsPromo)
class NewsPromoTranslationOptions(TranslationOptions):
    """Translate fields from model NewsPromo"""

    fields = ("name", "description")
    required_languages = ("uk", "ru")


@register(Page)
class PageTranslationOptions(TranslationOptions):
    """Translate fields from model Page"""

    fields = ("name", "content")
    required_languages = ("uk", "ru")


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    """Translate fields from model Tag"""

    fields = ("name",)
    required_languages = ("uk", "ru")
