"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import Constituency


@register(Constituency)
class ConstituencyTR(TranslationOptions):
    """Class declaring which fields of the Constituency model to translate."""

    fields = Constituency.translation_fields
