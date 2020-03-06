"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from home.translation_helper import add_language_content_panels
from .models import ToolsListingPage, ToolPage, ToolSubPage


@register(ToolsListingPage)
class ToolsListingPageTR(TranslationOptions):
    """A class to allow for the tools index page translation fields to be autopopulated in the database."""

    fields = ToolsListingPage.translation_fields


add_language_content_panels(ToolsListingPage)


@register(ToolPage)
class ToolPageTR(TranslationOptions):
    """A class to allow for the tool page translation fields to be autopopulated in the database."""

    fields = ToolPage.translation_fields


@register(ToolSubPage)
class ToolSubPageTR(TranslationOptions):
    """A class to allow for the tool sub-page translation fields to be autopopulated in the database."""

    fields = ToolSubPage.translation_fields


add_language_content_panels(ToolPage)
add_language_content_panels(ToolSubPage)
