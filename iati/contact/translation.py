"""Module for registering model fields for translation, for use by django-modeltranslation."""

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from home.translation_helper import add_language_content_panels
from .models import ContactPage


@register(ContactPage)
class ContactPageTR(TranslationOptions):
    fields = ContactPage.translation_fields


add_language_content_panels(ContactPage)
