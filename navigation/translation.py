"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .fields import Highlight


@register(Highlight)
class HighlightTR(TranslationOptions):
    """A class to allow for the highlight translation fields to be autopopulated in the database."""

    fields = Highlight.translation_fields
