"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from home.translation_helper import add_language_content_panels
from .models import UsingDataPage, ToolsIndexPage


@register(UsingDataPage)
class UsingDataPageTR(TranslationOptions):
    """Inheriting from AboutPage already comes with translations."""

    fields = UsingDataPage.translation_fields


add_language_content_panels(UsingDataPage)


@register(ToolsIndexPage)
class ToolsIndexPageTR(TranslationOptions):
    """Inheriting from AbstractContentPage already comes with translations."""

    fields = ToolsIndexPage.translation_fields


add_language_content_panels(ToolsIndexPage)
