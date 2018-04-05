from .models import Events
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(Events)
class EventsTR(TranslationOptions):
    fields = (
        'body',
    )
