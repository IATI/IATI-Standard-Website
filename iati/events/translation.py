from .models import EventIndexPage, EventPage, EventType
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
        'additional_information',
    )
    inline_fields = (
        'event_documents',
    )
    multilingual_fields = (
        'date_start',
        'date_end',
        'location',
        'registration_link',
    )
add_language_content_panels(EventPage,EventPageTR)


@register(EventType)
class EventTypeTR(TranslationOptions):
    fields = (
        'name',
    )
