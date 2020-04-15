"""Model definitions for the governance app."""

from django.conf import settings
from django import forms
from django.db import models
from django.db.models import Q
from django.shortcuts import render
from django.utils.functional import cached_property
from wagtail.admin.edit_handlers import InlinePanel, FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from common.utils import ForeignKeyField, WagtailImageField
from dashboard.edit_handlers import NoEmptyLabelFieldPanel
from home.models import AbstractContentPage
from governance.fields import MembersAssemblyFieldsMixin
from governance.inlines import *  # noqa
from taxonomies.models import Constituency
from taxonomies.utils import get_active_taxonomy_list


@register_snippet
class Member(index.Indexed, models.Model):
    """A snippet model for members."""

    class Meta:
        ordering = ['name']

    name = models.CharField(
        max_length=255,
        unique=True,
    )
    image = WagtailImageField(
        required=False,
        help_text='Optional: image for the member'
    )
    constituency = ForeignKeyField(
        model='taxonomies.Constituency',
        related_name='member',
        required=True,
        help_text='The constituency of the member',
    )
    url = models.URLField(
        max_length=255,
        blank=True,
        help_text='Optional: URL for the member',
    )
    date_joined = models.DateField(
        help_text='Year that the member joined'
    )
    active = models.BooleanField(
        blank=True,
        default=True,
        help_text='Only active members will be displayed on the site',
    )

    translation_fields = [
        'name',
    ]

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('image'),
        NoEmptyLabelFieldPanel(
            'constituency',
            widget=forms.RadioSelect,
            classname='non-floated-options',
        ),
        FieldPanel('url'),
        FieldPanel('date_joined'),
        FieldPanel('active'),
    ]

    def __str__(self):
        """Override magic method to return member name."""
        return self.name


class MembersAssemblyPage(MembersAssemblyFieldsMixin, RoutablePageMixin, AbstractContentPage):
    """A model for the members assembly page."""

    ORDERING = {
        'name': 'name',
        'date_joined': '-date_joined'
    }

    parent_page_types = ['about.AboutSubPage']
    subpage_types = []

    max_count = 1

    local_translation_fields = [
        'members_title',
    ]
    optional_local_translation_fields = [
    ]

    translation_fields = AbstractContentPage.translation_fields + local_translation_fields
    required_languages = {'en': list(set(local_translation_fields) - set(optional_local_translation_fields))}

    multilingual_field_panels = [
        InlinePanel(
            'chair_items',
            heading='Chair items',
            label='Chair item',
            max_num=1,
        ),
        InlinePanel(
            'vice_chair_items',
            heading='Vice chair items',
            label='Vice chair item',
        ),
    ]

    @cached_property
    def constituencies(self):
        """Return active constituency items."""
        return get_active_taxonomy_list(Constituency, {'member__isnull': False})

    def members(self, order):
        """Return all active member items, ordered by order argument."""
        return Member.objects.filter(active=True).order_by(order)

    def filtered_collection(self, constituency, order):
        """Return a filtered collection based on constituency, with some extra legwork for translation."""
        filters = {}
        filter_obj = Q()

        for item in settings.ACTIVE_LANGUAGES:
            filters['constituency__slug_%s' % item[0]] = constituency

        for item in filters:
            filter_obj |= Q(**{item: filters[item]})

        try:
            return (self
                    .members(order)
                    .filter(filter_obj)
                    .distinct())
        except Exception:
            return self.members(order)

    @route(r'^$')
    @route(r'^([-\w]+)/$')
    def index(self, request, constituency=None):
        """Return listing, filtering and ordering data based on the route variables."""
        context = self.get_context(request)

        # get the query string
        query = request.GET

        # pass back to context if not empty
        context['query'] = '?%s' % query.urlencode() if query else ''

        # get the order from the query, add ordering vars to context
        context['order'] = order_query = request.GET.get('order', self.ORDERING['name'])
        context['ordering'] = self.ORDERING

        # get the constituency from the path variable
        context['constituency'] = constituency if constituency else ''

        # add fragment id for filtered requests
        context['fragment'] = '#members'

        # get the members listing
        context['listing'] = self.filtered_collection(constituency, order_query) if constituency else self.members(order=order_query)

        return render(request, self.template, context)
