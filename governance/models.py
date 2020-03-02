"""Model definitions for the governance app."""

from django import forms
from django.db import models
from django.shortcuts import render
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

    def members(self, order):
        """Return the member items, ordered by order argument."""
        return Member.objects.all().order_by(order)

    def filtered_collection(self, constituency, order):
        filters = {
            'constituency__slug': constituency
        }

        try:
            return (self
                    .members(order)
                    .filter(**filters)
                    .distinct())
        except Exception:
            return self.members(order)

    @route(r'^$')
    @route(r'^([-\w]+)/$')
    def index(self, request, constituency=None):
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
