from django.db import models
from wagtail.core.models import Page, Orderable
from home.models import IATIStreamBlock
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldPanel, MultiFieldPanel, StreamFieldPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.fields import StreamField
from wagtail.snippets.models import register_snippet
from django.utils import translation
from django.utils import timezone
import pytz
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.documents.edit_handlers import DocumentChooserPanel

class EventIndexPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['events.EventPage']

    heading = models.CharField(max_length=255, null=True, blank=True)
    excerpt = models.TextField(null=True, blank=True)

    @property
    def events(self):
        "A function that queries the database for all EventPages that are children of the EventIndexPage and orders them by newest first."
        events = EventPage.objects.live().descendant_of(self)
        events = events.order_by('-date_start')
        return events

    def get_context(self, request):
        """Overwriting the default wagtail get_context function to allow for filtering based on params, including pagination.
           Try to display 5 events per page, but catch exceptions if the page is not a valid integer or we get an empty page.
        """
        events = self.events
        past = request.GET.get('past')
        now = timezone.now()
        if past:
            events = events.filter(date_start__lte=now)
        else:
            events = events.filter(date_start__gte=now)
        page = request.GET.get('page')
        paginator = Paginator(events, 5)
        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)
        context = super(EventIndexPage, self).get_context(request)
        context['events'] = events
        context['past'] = past
        return context


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
    additional_information = StreamField(IATIStreamBlock(required=False), null=True, blank=True)
    event_type = ParentalManyToManyField('events.EventType', blank=True)

    @property
    def event_type_concat(self):
        "A function that takes all of the EventType snippets and concatenates them into a space separated one-liner."
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


class EventDocument(Orderable):
    page = ParentalKey(EventPage, related_name='event_documents')
    document = models.ForeignKey(
        'wagtaildocs.Document', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        DocumentChooserPanel('document'),
    ]
