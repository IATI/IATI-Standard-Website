from .models import GuidanceAndSupport
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(GuidanceAndSupport)
class GuidanceAndSupportTR(TranslationOptions):
    pass
    # fields = (
    #     'body',
    # )
