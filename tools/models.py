"""Model definitions for the tools app."""

from django.db import models
from wagtail.images.edit_handlers import ImageChooserPanel
from home.models import AbstractIndexPage, AbstractContentPage, DefaultPageHeaderImageMixin


class ToolsIndexPage(DefaultPageHeaderImageMixin, AbstractIndexPage):
    """A model for tools index pages, the main tools landing page."""

    parent_page_types = ['home.HomePage']
    subpage_types = ['tools.ToolPage']


class ToolPage(AbstractContentPage):
    """A model for tool single pages."""

    parent_page_types = ['tools.ToolsIndexPage']
    subpage_types = []

    logo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    multilingual_field_panels = [
        ImageChooserPanel('logo'),
    ]
