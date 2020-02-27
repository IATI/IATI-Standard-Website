"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from home.translation_helper import add_language_content_panels
from .models import MembersAssemblyPage
from .inlines import ChairItems, ViceChairItems


@register(MembersAssemblyPage)
class MembersAssemblyPageTR(TranslationOptions):
    """A class to allow for the members assembly page translation fields to be autopopulated in the database."""

    fields = MembersAssemblyPage.translation_fields
    required_languages = MembersAssemblyPage.required_languages


add_language_content_panels(MembersAssemblyPage)


@register(ChairItems)
class ChairItemsTR(TranslationOptions):
    """Class declaring which fields of the ChairItems model to translate."""

    fields = ChairItems.translation_fields


@register(ViceChairItems)
class ViceChairItemsTR(TranslationOptions):
    """Class declaring which fields of the ViceChairItems model to translate."""

    fields = ViceChairItems.translation_fields
