from django.db import models
from wagtail.core.models import Page, Orderable
from home.models import IATIStreamBlock
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldPanel, MultiFieldPanel, StreamFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.fields import StreamField
from wagtail.snippets.models import register_snippet
from django.utils import translation
from django.utils import timezone
import pytz
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.documents.edit_handlers import DocumentChooserPanel
from django.utils.text import slugify
from django import forms
from wagtail.images.edit_handlers import ImageChooserPanel



from home.models import AbstractIndexPage, AbstractContentPage

class EventIndexPage(AbstractIndexPage):
    parent_page_types = ['home.HomePage']
    subpage_types = ['events.EventPage']

    @property
    def event_types(self):
        """A function to list all of the event types"""
        event_types = EventType.objects.all()
        return event_types


    def get_context(self, request):
        """Overwriting the default wagtail get_context function to allow for filtering based on params, including pagination.
           Use the functions built into the abstract index page class to dynamically filter the child pages and apply pagination, limiting the results to 3 per page.
        """
        filter_dict = {}
        children = EventPage.objects.live().descendant_of(self).order_by('-date_start')
        past = request.GET.get('past')
        now = timezone.now()
        if past:
            filter_dict["date_start__lte"] = now
        else:
            filter_dict["date_start__gte"] = now

        event_type = request.GET.get('event_type')
        if event_type:
            filter_dict["event_type__slug"] = event_type

        filtered_children = self.filter_children(children, filter_dict)
        paginated_children = self.paginate(request, filtered_children, 3)
        context = super(EventIndexPage, self).get_context(request)
        context['events'] = paginated_children
        context['past'] = past
        return context

    translation_fields = [
        'heading',
        'excerpt'
    ]


class EventPage(AbstractContentPage):
    parent_page_types = ['events.EventIndexPage']
    subpage_types = []

    date_start = models.DateTimeField("Event start date and time")
    date_end = models.DateTimeField("Event end date and time", null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    registration_link = models.URLField(max_length=255, null=True, blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    additional_information = StreamField(IATIStreamBlock(required=False), null=True, blank=True)
    event_type = ParentalManyToManyField('events.EventType', blank=True)

    @property
    def event_type_concat(self):
        "A function that takes all of the EventType snippets and concatenates them into a space separated one-liner."
        event_types = self.event_type.values_list('name', flat=True)

        return " | ".join(event_types)

    translation_fields = [
        'heading',
        'excerpt',
        'content_editor',
        'additional_information',
    ]

    multilingual_field_panels = [
        FieldPanel('date_start'),
        FieldPanel('date_end'),
        FieldPanel('location'),
        FieldPanel('registration_link'),
        FieldPanel('event_type', widget=forms.CheckboxSelectMultiple),
        ImageChooserPanel('feed_image'),
        InlinePanel('event_documents', label="Event attachments")
    ]


@register_snippet
class EventType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def full_clean(self, *args, **kwargs):
        """Apply fixups that need to happen before per-field validation occurs"""
        base_slug = slugify(self.name, allow_unicode=True)
        if base_slug:
            self.slug = base_slug
        super().full_clean(*args, **kwargs)
        
    translation_fields = [
        'name',
    ]

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
