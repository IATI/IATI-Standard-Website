"""Model definitions for the tools app."""

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Orderable
from home.models import AbstractContentPage, DefaultPageHeaderImageMixin


class ToolsIndexPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """A model for tools index pages, the main tools landing page."""

    parent_page_types = ['home.HomePage']
    subpage_types = ['tools.ToolPage']

    multilingual_field_panels = [
        InlinePanel(
            'featured_tools',
            label='Featured tools',
            help_text='Select and order the tools to be featured on the page.'
        )
    ]


class ToolPage(AbstractContentPage):
    """A model for tool single pages."""

    parent_page_types = ['tools.ToolsIndexPage']
    subpage_types = []

    logo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    external_url = models.URLField(
        max_length=255,
        blank=True,
        help_text='Optional: external URL of the tool',
    )

    multilingual_field_panels = [
        ImageChooserPanel('logo'),
        FieldPanel('external_url')
    ]


class FeaturedTool(Orderable):
    """A model for featured tool pages on the tools list."""

    page = ParentalKey(ToolPage, related_name='featured_tools')
    tool = models.ForeignKey(
        'tools.ToolPage',
        on_delete=models.CASCADE,
        related_name='+'
    )
    description = models.TextField(
        help_text='Short description for the listing'
    )

    panels = [
        PageChooserPanel('tool', 'tools.ToolPage'),
        FieldPanel('tool', 'tools.ToolPage'),
    ]
