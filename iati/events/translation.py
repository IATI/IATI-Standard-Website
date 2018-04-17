from .models import EventIndexPage, EventPage, EventType
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from home.translation_helper import add_language_content_panels

@register(EventIndexPage)
class EventIndexPageTR(TranslationOptions):
    fields = EventIndexPage.translation_fields
add_language_content_panels(EventIndexPage)


@register(EventPage)
class EventPageTR(TranslationOptions):
    fields = EventPage.translation_fields
add_language_content_panels(EventPage)


@register(EventType)
class EventTypeTR(TranslationOptions):
    fields = EventType.translation_fields
