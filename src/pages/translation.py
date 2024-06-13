from modeltranslation.translator import TranslationOptions, register

from src.pages.models import TopSliderItem, NewsPromo, Page


@register(TopSliderItem)
class TopSliderItemTranslationOptions(TranslationOptions):
    fields = ("text",)
    required_languages = ("uk", "ru")


@register(NewsPromo)
class NewsPromoTranslationOptions(TranslationOptions):
    fields = ("name", "description")
    required_languages = ("uk", "ru")


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ("name", "content")
    required_languages = ("uk", "ru")
