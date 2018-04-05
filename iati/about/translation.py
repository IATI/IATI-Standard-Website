from .models import About
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(About)
class AboutTR(TranslationOptions):
    fields = (
        'body',
    )
