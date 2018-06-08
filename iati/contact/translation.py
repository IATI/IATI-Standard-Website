from home.translation_helper import add_language_content_panels
from .models import ContactPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(ContactPage)
class ContactPageTR(TranslationOptions):
    fields = ContactPage.translation_fields


add_language_content_panels(ContactPage)
