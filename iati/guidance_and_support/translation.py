from .models import GuidanceAndSupportPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(GuidanceAndSupportPage)
class GuidanceAndSupportPageTR(TranslationOptions):
    pass
    # fields = (
    #     'body',
    # )
