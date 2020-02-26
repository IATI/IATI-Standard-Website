"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from home.translation_helper import add_language_content_panels
from .models import MembersAssemblyPage


@register(MembersAssemblyPage)
class MembersAssemblyPageTR(TranslationOptions):
    """A class to allow for the members assembly page translation fields to be autopopulated in the database."""

    fields = MembersAssemblyPage.translation_fields


add_language_content_panels(MembersAssemblyPage)
