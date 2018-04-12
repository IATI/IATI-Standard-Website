from .models import EventIndexPage, EventPage, EventType
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, InlinePanel
from django import forms

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
    multilingual_field_panels = (
        FieldPanel('date_start'),
        FieldPanel('date_end'),
        FieldPanel('location'),
        FieldPanel('registration_link'),
        FieldPanel('event_type', widget=forms.CheckboxSelectMultiple),
        ImageChooserPanel('feed_image'),
        InlinePanel('event_documents',label="Event attachments")
    )
add_language_content_panels(EventPage,EventPageTR)


@register(EventType)
class EventTypeTR(TranslationOptions):
    fields = (
        'name',
    )
