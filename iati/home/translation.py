from .models import HomePage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from home.translation_helper import add_language_content_panels


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = HomePage.translation_fields


add_language_content_panels(HomePage)
