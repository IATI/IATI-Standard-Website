"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from home.translation_helper import add_language_content_panels
from .models import ToolsIndexPage, ToolPage


@register(ToolsIndexPage)
class ToolsIndexPageTR(TranslationOptions):
    """A class to allow for the news index page translation fields to be autopopulated in the database."""

    fields = ToolsIndexPage.translation_fields


add_language_content_panels(ToolsIndexPage)


@register(ToolPage)
class ToolPageTR(TranslationOptions):
    """A class to allow for the news page translation fields to be autopopulated in the database."""

    fields = ToolPage.translation_fields


add_language_content_panels(ToolPage)
