"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from home.translation_helper import strip_non_english
from .models import PrimaryMenuLinks, UtilityMenuLinks, UsefulLinksMenu


@register(PrimaryMenuLinks)
class PrimaryMenuLinksTR(TranslationOptions):
    """Class declaring which fields of the PrimaryMenuLinks model to translate."""

    fields = PrimaryMenuLinks.translation_fields


@register(UtilityMenuLinks)
class UtilityMenuLinksTR(TranslationOptions):
    """Class declaring which fields of the UtilityMenuLinks model to translate."""

    fields = UtilityMenuLinks.translation_fields


@register(UsefulLinksMenu)
class UsefulLinksMenuTR(TranslationOptions):
    """Class declaring which fields of the UsefulLinksMenu model to translate."""

    fields = UsefulLinksMenu.translation_fields


strip_non_english(PrimaryMenuLinks)
strip_non_english(UtilityMenuLinks)
strip_non_english(UsefulLinksMenu)
