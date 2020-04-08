"""Model definitions for the events app."""

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


class EventIndexPage(DefaultPageHeaderImageMixin, AbstractIndexPage):
    """A model for event index pages, the main event landing page."""

    parent_page_types = ['home.HomePage']
    subpage_types = ['events.EventPage']

    max_count = 1

    @property
    def event_types(self):
        """List all of the event types."""
        event_types = EventType.objects.all()
        return event_types

    def get_events(self, request, filter_dict=None, order_by=None):
        """Return a filtered and paginated list of events."""
        if order_by:
            all_events = EventPage.objects.live().descendant_of(self).order_by(*order_by)
        else:
            all_events = EventPage.objects.live().descendant_of(self).order_by('date_start')
        if filter_dict:
            filtered_events = self.filter_children(all_events, filter_dict)
        else:
            filtered_events = all_events
        paginated_events = self.paginate(request, filtered_events, 3)
        return paginated_events

    def get_context(self, request, *args, **kwargs):
        """Overwrite the default wagtail get_context function to allow for filtering based on params, including pagination.

        Use the functions built into the abstract index page class to dynamically filter the child pages and apply pagination, limiting the results to 3 per page.

        """
        final_valid_day_begin = timezone.datetime.combine(timezone.now(), timezone.datetime.min.time())
        filter_dict = {}
        archive_years = EventPage.objects.live().descendant_of(self).filter(date_end__lte=final_valid_day_begin).dates('date_end', 'year', order='DESC')
        past = request.GET.get('past') == "1"
        if past:
            filter_dict["date_end__lt"] = final_valid_day_begin  # an event is in the past if it ended before today's 00:00am
            order_by = ['-date_start']
        else:
            filter_dict["date_end__gte"] = final_valid_day_begin  # an event stays as current/future till end date is prior to today's 11:59pm
            order_by = ['-featured_event', 'date_start']

        try:
            year = int(request.GET.get('year'))
        except (TypeError, ValueError):
            year = None
        if year:
            filter_dict["date_start__year"] = year

        event_type = request.GET.get('event_type')
        if event_type:
            filter_dict["event_type__slug"] = event_type

        if request.LANGUAGE_CODE:
            filter_dict["title_{}__isnull".format(request.LANGUAGE_CODE)] = False

        context = super(EventIndexPage, self).get_context(request)
        context['events'] = self.get_events(request, filter_dict, order_by)
        context['paginator_range'] = self._get_paginator_range(context['events'])
        context['past'] = past
        context['archive_years'] = archive_years
        if past:
            heading = context['page'].heading
            past_heading = "Past " + heading if heading is not None else None
            setattr(context['page'], "heading", past_heading)
        return context


class EventPage(AbstractContentPage):
    """A model for event single pages."""

    parent_page_types = ['events.EventIndexPage']
    subpage_types = []

    featured_event = models.BooleanField(default=False)
    date_start = models.DateTimeField("Event start date and time", default=timezone.now)
    date_end = models.DateTimeField("Event end date and time", null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    registration_link = models.URLField(max_length=255, null=True, blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+',
        help_text='This is the image that will be displayed for the event in the page header and on the Events and Past Events list pages.'
    )

    additional_information = StreamField(IATIStreamBlock(required=False), null=True, blank=True)
    event_type = ParentalManyToManyField('events.EventType', blank=True)

    @property
    def event_type_concat(self):
        """Take all of the EventType snippets and concatenate them into a space separated one-liner."""
        event_types = self.event_type.values_list('name', flat=True)

        return " | ".join(event_types)

    translation_fields = AbstractContentPage.translation_fields + ["additional_information"]

    multilingual_field_panels = [
        FieldPanel('featured_event'),
        FieldPanel('date_start'),
        FieldPanel('date_end'),
        FieldPanel('location'),
        FieldPanel('registration_link'),
        FieldPanel('event_type', widget=forms.CheckboxSelectMultiple),
        ImageChooserPanel('feed_image'),
    ]

    @property
    def search_display_date(self):
        """Return a date for search display."""
        DATE_FORMAT = '%-d %b %Y'
        start_date = self.date_start.date()
        end_date = self.date_end.date()
        dates = start_date.strftime(DATE_FORMAT)
        if start_date != end_date:
            dates = '%s - %s' % (start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT))

        return 'Date: %s' % dates


@register_snippet
class EventType(models.Model):
    """A snippet model for event types, to be added in the snippet menu prior to creating events for uniformity."""

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        """Override magic method to return event type name."""
        return self.name

    def full_clean(self, exclude=None, validate_unique=True):
        """Apply fixups that need to happen before per-field validation occurs."""
        base_slug = slugify(self.name, allow_unicode=True)
        if base_slug:
            self.slug = base_slug
        super(EventType, self).full_clean(exclude, validate_unique)

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Call full_clean method for slug validation."""
        self.full_clean()
        super().save(*args, **kwargs)

    translation_fields = ['name']

    panels = [FieldPanel('name')]


@register_snippet
class FeaturedEvent(models.Model):
    """A snippet model for featured events, with a page chooser that only allows event pages to be selected."""

    event = models.ForeignKey('events.EventPage', on_delete=models.CASCADE, related_name="+")

    def __str__(self):
        """Override magic method to return event heading and start date."""
        return "{0} on {1}".format(self.event.heading, _date(self.event.date_start))

    panels = [
        PageChooserPanel('event', 'events.EventPage')
    ]
