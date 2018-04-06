from .models import EventIndexPage, EventPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(EventIndexPage)
class EventIndexPageTR(TranslationOptions):
    fields = (
        'heading',
        'excerpt'
    )
    
@register(EventPage)
class EventPageTR(TranslationOptions):
    fields = (
        'heading',
        'subheading',
        'description',
        'additional_information'
    )
