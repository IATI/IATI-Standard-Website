from .models import EventIndexPage, EventPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from home.translation_helper import add_language_content_panels

@register(EventIndexPage)
class EventIndexPageTR(TranslationOptions):
    fields = (
        'heading',
        'excerpt'
    )
add_language_content_panels(EventIndexPage,EventIndexPageTR)
    
@register(EventPage)
class EventPageTR(TranslationOptions):
    fields = (
        'heading',
        'subheading',
        'description',
        'additional_information'
    )
add_language_content_panels(EventPage,EventPageTR)
