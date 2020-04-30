"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import GlobalNotice, PageNotice


@register(GlobalNotice)
class GlobalNoticeTR(TranslationOptions):
    """Class declaring which fields of the GlobalNotice model to translate."""

    fields = GlobalNotice.translation_fields


@register(PageNotice)
class PageNoticeTR(TranslationOptions):
    """Class declaring which fields of the PageNotice model to translate."""

    fields = PageNotice.translation_fields
