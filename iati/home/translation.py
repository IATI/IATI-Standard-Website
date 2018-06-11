from .models import HomePage, StandardPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from home.translation_helper import add_language_content_panels


@register(HomePage)
class HomePageTR(TranslationOptions):
    pass
add_language_content_panels(HomePage)


@register(StandardPage)
class StandardPageTR(TranslationOptions):
    fields = StandardPage.translation_fields
add_language_content_panels(StandardPage)
