"""Model definitions for the iati_standard app."""

from bs4 import BeautifulSoup

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property
from django.utils.text import slugify

from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, PageChooserPanel, TabbedInterface
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.search.index import SearchField
from wagtail.core.blocks import (
    CharBlock,
    PageChooserBlock,
    StreamBlock,
    StructBlock
)

from home.models import AbstractContentPage, AbstractIndexPage, DefaultPageHeaderImageMixin

from iati_standard.panels import ReferenceDataPanel


class CardBlock(StructBlock):
    """A class to construct the card block streamfield for the IATI Standard Page."""

    major_header = CharBlock(
        required=False,
        help_text='Text for the header element of the card'
    )
    card_content = StreamBlock([
        ('minor_header', CharBlock(template='iati_standard/blocks/minor_header.html', required=False, icon='title')),
        ('page_links', StreamBlock([
            ('page', PageChooserBlock(template='iati_standard/blocks/page_link.html', required=False))
        ], template='iati_standard/blocks/page_links.html')),
    ])

    class Meta():
        template = 'iati_standard/blocks/card_block.html'


class IATIStandardPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """A model for the IATI Standard Page, a landing page for IATI reference."""

    parent_page_types = ['home.HomePage']
    subpage_types = []

    max_count = 1

    repo = models.URLField(
        help_text='Git repo URL',
        blank=True,
        null=True
    )

    live_tag = models.CharField(
        max_length=255,
        help_text='Associated git release tag',
        blank=True,
        null=True
    )

    guidance_parent_page = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True
    )

    latest_version_page = models.ForeignKey(
        'iati_standard.ActivityStandardPage',
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True
    )
    reference_support_page = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True
    )

    static = models.BooleanField(
        default=True,
        help_text="If true, retain static links. Otherwise use dynamic links."
    )

    how_to_use_page = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True
    )

    reference_cards = StreamField([
        ('card', CardBlock())
    ], null=True, blank=True)

    multilingual_field_panels = DefaultPageHeaderImageMixin.multilingual_field_panels + [
        FieldPanel('static'),
        PageChooserPanel('latest_version_page', 'iati_standard.ActivityStandardPage'),
        PageChooserPanel('reference_support_page'),
        PageChooserPanel('how_to_use_page'),
        StreamFieldPanel('reference_cards'),
        ReferenceDataPanel()
    ]


@register_snippet
class StandardGuidanceType(models.Model):
    """A snippet model for standard guidance types."""

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
        super(StandardGuidanceType, self).full_clean(exclude, validate_unique)

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Call full_clean method for slug validation."""
        self.full_clean()
        super().save(*args, **kwargs)

    panels = [FieldPanel('name')]


class StandardGuidanceIndexPage(DefaultPageHeaderImageMixin, AbstractIndexPage):
    """A model for standard guidance index page."""

    parent_page_types = ['guidance_and_support.GuidanceAndSupportPage']
    subpage_types = ['iati_standard.StandardGuidancePage']

    max_count = 1

    @property
    def guidance_types(self):
        """List all of the event types."""
        guidance_types = StandardGuidanceType.objects.all()
        return guidance_types

    def get_guidance(self, request, filter_dict=None):
        """Return a filtered and paginated list of events."""
        all_guidance = StandardGuidancePage.objects.live().descendant_of(self).order_by('title')
        if filter_dict:
            filtered_guidance = self.filter_children(all_guidance, filter_dict)
        else:
            filtered_guidance = all_guidance
        paginated_guidance = self.paginate(request, filtered_guidance, 16)
        return paginated_guidance

    def get_context(self, request, *args, **kwargs):
        """Overwrite the default wagtail get_context function to allow for filtering based on params, including pagination.

        Use the functions built into the abstract index page class to dynamically filter the child pages and apply pagination, limiting the results to 3 per page.

        """
        filter_dict = {}

        guidance_types = request.GET.get('guidance_type')
        if guidance_types:
            guidance_type_list = guidance_types.split(",")
            filter_dict["guidance_type__slug__in"] = guidance_type_list

        context = super(StandardGuidanceIndexPage, self).get_context(request)
        context['guidance'] = self.get_guidance(request, filter_dict)
        context['paginator_range'] = self._get_paginator_range(context['guidance'])
        return context


@register_snippet
class ReferenceData(models.Model):
    """A model to act as a temporary holding place for SSOT data."""

    class Meta:
        """Metadata class."""

        ordering = ['ssot_path']
        verbose_name_plural = 'Reference data'
        unique_together = ['ssot_path', 'tag']

    ssot_path = models.TextField(
        null=True,
        blank=True,
        help_text='Folder path of SSOT object'
    )

    tag = models.CharField(
        max_length=255,
        help_text='Associated git release tag',
    )

    language = models.CharField(
        max_length=255,
        help_text='Language',
        default="en"
    )

    ssot_root_slug = models.CharField(
        max_length=255,
        help_text='Slug of the highest parent folder.'
    )

    parent_path = models.TextField(
        null=True,
        blank=True,
        help_text='Parent path of object'
    )

    data = models.TextField(
        null=True,
        blank=True,
        help_text='HTML data for the page'
    )

    @cached_property
    def name(self):
        """Return the last item in the ssot_path as a name."""
        return self.ssot_path.split("/")[-1]

    def __str__(self):
        """Print full path as name."""
        return self.ssot_path

    def save(self, *args, **kwargs):
        """Overwrite save to automatically update parent_path."""
        self.parent_path = "/".join(self.ssot_path.split("/")[:-1])
        self.ssot_root_slug = self.ssot_path.split("/")[0]
        super(ReferenceData, self).save(*args, **kwargs)


class ActivityStandardPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """A model for reference to the Activity Standard."""

    is_creatable = False
    edit_handler = TabbedInterface([])

    parent_page_types = []
    subpage_types = []

    ssot_path = models.TextField(
        null=True,
        blank=True,
        help_text='Folder path of SSOT object'
    )

    tag = models.CharField(
        max_length=255,
        help_text='Associated git release tag',
    )

    data = models.TextField(
        null=True,
        blank=True,
        help_text='HTML data for the page'
    )

    translation_fields = AbstractContentPage.translation_fields + ["data"]
    search_fields = AbstractContentPage.search_fields + [
        SearchField('data'),
    ]

    @cached_property
    def parent_path(self):
        """Return ssot_path of parent object."""
        return "/".join(self.ssot_path.split("/")[:-1])

    @cached_property
    def name(self):
        """Return the last item in the ssot_path as a name."""
        return self.ssot_path.split("/")[-1]

    @cached_property
    def version(self):
        """Return the first item in the ssot_path as a version."""
        return self.ssot_path.split("/")[0]

    def save(self, *args, **kwargs):
        """Overwrite save to automatically update title."""
        soup = BeautifulSoup(self.data, 'html.parser')
        title = soup.find("h1")
        if title:
            self.title = title.text.replace("¶", "")
            self.heading = title.text.replace("¶", "")
        super(ActivityStandardPage, self).save(*args, **kwargs)


class StandardGuidancePage(ActivityStandardPage):
    template = 'iati_standard/standard_guidance_page.html'


class ReferenceMenu(models.Model):
    """A model for to store the Standard Reference menu."""

    tag = models.CharField(
        max_length=255,
        help_text='Associated git release tag',
    )

    menu_json = JSONField()
