"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import SearchPage


@register(SearchPage)
class SearchPageTR(TranslationOptions):
    """Class declaring which fields of the SearchPage model to translate."""

    fields = SearchPage.translation_fields
