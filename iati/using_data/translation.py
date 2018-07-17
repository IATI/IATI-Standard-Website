"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from home.translation_helper import add_language_content_panels
from .models import UsingDataPage


@register(UsingDataPage)
class UsingDataPageTR(TranslationOptions):
    """Inheriting from AboutPage already comes with translations."""

    fields = list()


add_language_content_panels(UsingDataPage)
