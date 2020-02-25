"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from home.translation_helper import add_language_content_panels
from .models import GetInvolvedPage


@register(GetInvolvedPage)
class GetInvolvedPageTR(TranslationOptions):
    """A class to allow for the get involved page translation fields to be autopopulated in the database."""

    fields = GetInvolvedPage.translation_fields


add_language_content_panels(GetInvolvedPage)
