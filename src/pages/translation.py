from modeltranslation.translator import TranslationOptions, register

from src.pages.models import TopSliderItem


@register(TopSliderItem)
class TopSliderItemTranslationOptions(TranslationOptions):
    fields = ("text",)
    required_languages = ("uk", "ru")

