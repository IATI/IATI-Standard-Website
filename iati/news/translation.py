from .models import News
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(News)
class NewsTR(TranslationOptions):
    fields = (
        'body',
    )
