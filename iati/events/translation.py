from .models import EventIndexPage, EventPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(EventIndexPage)
class EventIndexPageTR(TranslationOptions):
    pass
    # fields = (
    #     'body',
    # )
    
@register(EventPage)
class EventPageTR(TranslationOptions):
    pass
    # fields = (
    #     'body',
    # )
