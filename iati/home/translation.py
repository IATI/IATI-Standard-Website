from .models import HomePage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from wagtail.core.models import Page

from home.translation_helper import add_language_content_panels

@register(HomePage)
class HomePageTR(TranslationOptions):
    pass
add_language_content_panels(HomePage, HomePageTR)
