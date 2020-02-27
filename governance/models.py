"""Model definitions for the governance app."""

from django import forms
from django.db import models
from wagtail.admin.edit_handlers import InlinePanel, FieldPanel
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


class MembersAssemblyPage(MembersAssemblyFieldsMixin, AbstractContentPage):
    """A model for the members assembly page."""

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
