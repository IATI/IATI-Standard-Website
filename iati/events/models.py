from django import forms
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.template.defaultfilters import date as _date
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.fields import StreamField
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel
from home.models import AbstractIndexPage, AbstractContentPage, DefaultPageHeaderImageMixin, IATIStreamBlock


class EventIndexPage(DefaultPageHeaderImageMixin, AbstractIndexPage):  # pylint: disable=too-many-ancestors
    """A model for event index pages, the main event landing page."""

    parent_page_types = ['home.HomePage']
    subpage_types = ['events.EventPage']

    @property
    def event_types(self):
        """A function to list all of the event types"""
        event_types = EventType.objects.all()
        return event_types

    def get_context(self, request, *args, **kwargs):
        """Overwriting the default wagtail get_context function to allow for filtering based on params, including pagination.

        Use the functions built into the abstract index page class to dynamically filter the child pages and apply pagination, limiting the results to 3 per page.

        """
        now = timezone.now()
        filter_dict = {}
        children = EventPage.objects.live().descendant_of(self).order_by('-date_start')
        archive_years = EventPage.objects.live().descendant_of(self).filter(date_start__lte=now).dates('date_start', 'year', order='DESC')
        past = request.GET.get('past') == "1"
        if past:
            filter_dict["date_start__lte"] = now
        else:
            filter_dict["date_start__gte"] = now

        try:
            year = int(request.GET.get('year'))
        except (TypeError, ValueError):
            year = None
        if year:
            filter_dict["date_start__year"] = year

        event_type = request.GET.get('event_type')
        if event_type:
            filter_dict["event_type__slug"] = event_type

        filtered_children = self.filter_children(children, filter_dict)
        paginated_children = self.paginate(request, filtered_children, 3)
        context = super(EventIndexPage, self).get_context(request)
        context['events'] = paginated_children
        context['past'] = past
        context['archive_years'] = archive_years
        if past:
            heading = context['page'].heading
            past_heading = "Past " + heading if heading is not None else None
            setattr(context['page'], "heading", past_heading)
        return context


class EventPage(AbstractContentPage):  # pylint: disable=too-many-ancestors
    """A model for event single pages"""

    parent_page_types = ['events.EventIndexPage']
    subpage_types = []

    date_start = models.DateTimeField("Event start date and time", default=timezone.now)
    date_end = models.DateTimeField("Event end date and time", null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    registration_link = models.URLField(max_length=255, null=True, blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='This is the image that will be displayed for the event in the page header and on the Events and Past Events list pages.'
    )

    additional_information = StreamField(IATIStreamBlock(required=False), null=True, blank=True)
    event_type = ParentalManyToManyField('events.EventType', blank=True)

    @property
    def event_type_concat(self):
        """A function that takes all of the EventType snippets and concatenates them into a space separated one-liner."""
        event_types = self.event_type.values_list('name', flat=True)

        return " | ".join(event_types)

    translation_fields = AbstractContentPage.translation_fields + ["additional_information"]

    multilingual_field_panels = [
        FieldPanel('date_start'),
        FieldPanel('date_end'),
        FieldPanel('location'),
        FieldPanel('registration_link'),
        FieldPanel('event_type', widget=forms.CheckboxSelectMultiple),
        ImageChooserPanel('feed_image'),
    ]


@register_snippet
class EventType(models.Model):
    """A snippet model for event types, to be added in the snippet menu prior to creating events for uniformity."""

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        """Explicit to string function"""
        return self.name

    def full_clean(self, exclude=None, validate_unique=True):
        """Apply fixups that need to happen before per-field validation occurs"""
        base_slug = slugify(self.name, allow_unicode=True)
        if base_slug:
            self.slug = base_slug
        super(EventType, self).full_clean(exclude, validate_unique)

    translation_fields = [
        'name',
    ]

    panels = [
        FieldPanel('name'),
    ]


@register_snippet
class FeaturedEvent(models.Model):
    """A snippet model for featured events, with a page chooser that only allows event pages to be selected."""

    event = models.ForeignKey('events.EventPage', on_delete=models.CASCADE, related_name="+")

    def __str__(self):
        return self.event.heading + " on " + _date(self.event.date_start)

    panels = [
        PageChooserPanel('event', 'events.EventPage')
    ]
