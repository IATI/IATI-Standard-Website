"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from home.translation_helper import add_language_content_panels
from .models import IATIStandardPage


@register(IATIStandardPage)
class IATIStandardPageTR(TranslationOptions):
    """Class declaring which fields of the IATIStandardPage model to translate."""

    fields = IATIStandardPage.translation_fields


add_language_content_panels(IATIStandardPage)
