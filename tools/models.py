"""Model definitions for the tools app."""

from django.db import models
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, PageChooserPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Orderable
from wagtail.fields import RichTextField
from home.models import AbstractContentPage, DefaultPageHeaderImageMixin


class ToolsListingPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """A model for tools index pages, the main tools landing page."""

    parent_page_types = ['home.HomePage']
    subpage_types = ['tools.ToolPage']

    max_count = 1

    highlight_title = models.CharField(
        max_length=255,
        blank=True,
        help_text='Optional: title for the highlight panel displayed after featured tools',
    )
    highlight_content = RichTextField(
        features=['link'],
        blank=True,
        help_text='Optional: content for the highlight panel displayed after featured tools',
    )

    content_panels = AbstractContentPage.content_panels + DefaultPageHeaderImageMixin.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('featured_tools', label='Featured tool', help_text='Select and order the tools to be featured on the page.'),
            ],
            heading='Featured tools',
        ),
        FieldPanel('highlight_title'),
        FieldPanel('highlight_content'),
    ]

    @cached_property
    def tools(self):
        """Return a list of selected featured tools, if tool is live."""
        tools = self.featured_tools.all()
        if self.live:
            tools = [x for x in tools if x.tool.live]
        return tools

    @cached_property
    def highlight(self):
        """Return True if both highlight title and content are present."""
        return self.highlight_title and self.highlight_content


class AbstractToolPage(AbstractContentPage):
    """An abstract model for tool single pages."""

    class Meta:
        abstract = True

    logo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    listing_description = models.CharField(
        max_length=999,
        blank=True,
        help_text='Optional: short description to appear on the listing page if this tool is featured',
    )
    external_url = models.URLField(
        max_length=999,
        blank=True,
        help_text='Optional: external URL of the tool',
    )
    button_label = models.CharField(
        max_length=999,
        blank=True,
        help_text='Optional: label for the external URL button',
    )

    content_panels = AbstractContentPage.content_panels + [
        FieldPanel('logo'),
        FieldPanel('external_url'),
        FieldPanel('listing_description'),
        FieldPanel('button_label')
    ]


class ToolPage(AbstractToolPage):
    """A model for tool single pages."""

    parent_page_types = ['tools.ToolsListingPage']
    subpage_types = ['tools.ToolSubPage']


class ToolSubPage(AbstractToolPage):
    """A model for tool sub-pages."""

    template = 'tools/tool_page.html'

    parent_page_types = ['tools.ToolPage', 'tools.ToolSubPage']
    subpage_types = ['tools.ToolSubPage']


class FeaturedTool(Orderable):
    """A model for featured tool pages on the tools list."""

    page = ParentalKey(ToolsListingPage, related_name='featured_tools')
    tool = models.ForeignKey(
        'tools.ToolPage',
        on_delete=models.CASCADE,
        related_name='+'
    )

    panels = [
        PageChooserPanel('tool', 'tools.ToolPage'),
    ]
