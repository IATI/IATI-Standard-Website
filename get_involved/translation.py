"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from home.translation_helper import add_language_content_panels
from .models import GetInvolvedPage
from .inlines import GetInvolvedItems


@register(GetInvolvedPage)
class GetInvolvedPageTR(TranslationOptions):
    """A class to allow for the get involved page translation fields to be autopopulated in the database."""

    fields = GetInvolvedPage.translation_fields


add_language_content_panels(GetInvolvedPage)


@register(GetInvolvedItems)
class GetInvolvedItemsTR(TranslationOptions):
    """Class declaring which fields of the GetInvolvedItems model to translate."""

    fields = GetInvolvedItems.translation_fields
