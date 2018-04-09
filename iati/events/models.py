from django.db import models
from wagtail.core.models import Page
from home.models import TranslatedField, IATIStreamBlock
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldPanel, MultiFieldPanel, StreamFieldPanel
from modelcluster.fields import ParentalManyToManyField
from wagtail.core.fields import StreamField
from wagtail.snippets.models import register_snippet
from django.utils import translation


class EventIndexPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['events.EventPage']

    # Heading

    heading = models.CharField(max_length=255, null=True, blank=True)

    # Excerpt

    excerpt = models.TextField(null=True, blank=True)

    @property
    def events(self):
        "Add docstring here."
        # Get list of live event pages that are descendents of this page
        events = EventPage.objects.live().descendant_of(self)

        # Order by most recent
        events = events.order_by('-date_start')

        return events


class EventPage(Page):
    parent_page_types = ['events.EventIndexPage']
    subpage_types = []

    date_start = models.DateTimeField("Event start date and time")
    date_end = models.DateTimeField("Event end date and time", null=True, blank=True)

    location = models.TextField(null=True, blank=True)

    registration_link = models.URLField(max_length=255, null=True, blank=True)

    heading = models.TextField(null=True, blank=True)

    subheading = models.TextField(null=True, blank=True)

    description = StreamField(IATIStreamBlock(required=False), null=True, blank=True)

    # additional_information

    additional_information = StreamField(IATIStreamBlock(required=False), null=True, blank=True)

    event_type = ParentalManyToManyField('events.EventType', blank=True)

    @property
    def event_type_concat(self):
        "Add docstring here."
        event_types = self.event_type.values_list('name', flat=True)

        return " ".join(event_types)


@register_snippet
class EventType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
    ]
