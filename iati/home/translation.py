from .models import Home
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(Home)
class HomeTR(TranslationOptions):
    fields = (
        'body',
    )
