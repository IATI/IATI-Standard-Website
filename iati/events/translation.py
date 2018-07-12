from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from home.translation_helper import add_language_content_panels
from .models import EventIndexPage, EventPage, EventType


@register(EventIndexPage)
class EventIndexPageTR(TranslationOptions):
    """A class to allow for the event index page translation fields to be autopopulated in the database."""
    fields = EventIndexPage.translation_fields


add_language_content_panels(EventIndexPage)


@register(EventPage)
class EventPageTR(TranslationOptions):
    """A class to allow for the event page translation fields to be autopopulated in the database."""
    fields = EventPage.translation_fields


add_language_content_panels(EventPage)


@register(EventType)
class EventTypeTR(TranslationOptions):
    """A class to allow for the event type snippet translation fields to be autopopulated in the database."""
    fields = EventType.translation_fields
