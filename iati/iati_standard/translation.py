from .models import IATIStandardPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from home.translation_helper import add_language_content_panels


@register(IATIStandardPage)
class IATIStandardPageTR(TranslationOptions):
    fields = IATIStandardPage.translation_fields


add_language_content_panels(IATIStandardPage)