"""Model definitions for the iati_standard app."""

import os
from bs4 import BeautifulSoup
from datetime import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property
from django.template.defaultfilters import date

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, PageChooserPanel, TabbedInterface
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.search.models import Query
from wagtail.search.index import SearchField, FilterField
from wagtail.snippets.models import register_snippet
from wagtail.core.blocks import (
    CharBlock,
    PageChooserBlock,
    StreamBlock,
    StructBlock
)

from home.models import AbstractContentPage, AbstractIndexPage, DefaultPageHeaderImageMixin, IATIStreamBlock

from iati_standard.panels import ReferenceDataPanel
from iati_standard.inlines import StandardGuidanceTypes
from iati_standard.widgets import JSONFieldWidget


class SyncTaskResult(models.Model):
    """Replacement for Celery task result."""

    task_id = models.AutoField(primary_key=True)
    state = models.TextField(default='PENDING')
    info = models.TextField(blank=True)

    def update_state(self, state, meta=""):
        """Imitate the update_state function of an asyncronous task runner."""
        self.state = state
        self.info = meta
        self.save()


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


class StandardGuidanceIndexPage(DefaultPageHeaderImageMixin, AbstractIndexPage):
    """A model for standard guidance index page."""

    parent_page_types = ['guidance_and_support.GuidanceAndSupportPage']
    subpage_types = ['iati_standard.StandardGuidancePage']

    max_count = 1

    section_summary = models.TextField(
        blank=True,
        null=True,
        help_text='Summary seen on Guidance and Support page'
    )
    button_link_text = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        help_text='Button text to be shown on Guidance and Support page',
    )

    content_editor = StreamField(IATIStreamBlock(required=False), null=True, blank=True)

    translation_fields = AbstractIndexPage.translation_fields + ["section_summary", "button_link_text", "content_editor"]

    def get_guidance(self, request, filter_dict=None, search_query=None):
        """Return a filtered list of guidance."""
        all_guidance = StandardGuidancePage.objects.live().descendant_of(self).order_by('title')
        if filter_dict:
            filtered_guidance = self.filter_children(all_guidance, filter_dict)
        else:
            filtered_guidance = all_guidance
        if search_query and filtered_guidance:
            queried_guidance = all_guidance.filter(
                id__in=filtered_guidance.values_list('id', flat=True)
            ).search(
                search_query,
                order_by_relevance=False
            )
        else:
            queried_guidance = filtered_guidance
        return queried_guidance

    def get_context(self, request, *args, **kwargs):
        """Overwrite the default wagtail get_context function to allow for filtering based on params.

        Use the functions built into the abstract index page class to dynamically filter the child pages.

        """
        filter_dict = {}

        search_query = request.GET.get('search', None)
        if search_query:
            query = Query.get(search_query)
            query.add_hit()

        guidance_type_organisation = request.GET.get('organisation', None)
        guidance_type_activity = request.GET.get('activity', None)
        guidance_type_list = list()
        if guidance_type_organisation:
            guidance_type_list.append("organisation")
        if guidance_type_activity:
            guidance_type_list.append("activity")
        if len(guidance_type_list):
            filter_dict["guidance_types__guidance_type__in"] = guidance_type_list

        context = super(StandardGuidanceIndexPage, self).get_context(request)
        context['guidance'] = self.get_guidance(request, filter_dict, search_query)
        return context


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


class AbstractGithubPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """A model for abstract reference pages build by Github."""

    class Meta(object):
        """Meta data for the class."""

        abstract = True

    is_creatable = False
    edit_handler = TabbedInterface([])

    parent_page_types = []
    subpage_types = []

    meta_order = models.IntegerField(
        default=0
    )

    ssot_path = models.TextField(
        null=True,
        blank=True,
        help_text='Folder path of SSOT object'
    )

    tag = models.CharField(
        max_length=255,
        help_text='Associated git release tag',
    )

    ssot_root_slug = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Slug of the highest parent folder.'
    )

    data = models.TextField(
        null=True,
        blank=True,
        help_text='HTML data for the page'
    )

    publish_date = models.TextField(
        null=True,
        blank=True
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

    def first_paragraph(self):
        """Extract first paragraph snippet."""
        soup = BeautifulSoup(self.data, 'html.parser')
        para = soup.find("p")
        if para:
            first_paragraph = para.text.replace("¶", "")
        else:
            first_paragraph = "Read more about {}.".format(self.title)
            return first_paragraph
        fp_split = first_paragraph.split(" ")
        fp_trunc = ""
        if len(fp_split) >= 50:
            fp_trunc = "..."
        first_paragraph = " ".join(first_paragraph.split(" ")[:50]) + fp_trunc
        return first_paragraph

    def save(self, *args, **kwargs):
        """Overwrite save to automatically update title."""
        soup = BeautifulSoup(self.data, 'html.parser')
        meta_order = soup.find("meta", {"name": "order"})
        if meta_order:
            try:
                self.meta_order = int(meta_order["content"])
            except ValueError:
                self.meta_order = 0
        meta_date = soup.find("meta", {"name": "date"})
        if meta_date:
            self.publish_date = meta_date["content"]
        else:
            self.publish_date = date(datetime.now(), "F d, Y")
        meta_title = soup.find("meta", {"name": "title"})
        if meta_title:
            self.title = meta_title["content"].replace("¶", "")
            self.heading = meta_title["content"].replace("¶", "")
        else:
            title = soup.find("h1")
            if title:
                self.title = title.text.replace("¶", "")
                self.heading = title.text.replace("¶", "")
        meta_description = soup.find("meta", {"name": "description"})
        if meta_description:
            self.excerpt = meta_description["content"].replace("¶", "")
        else:
            self.excerpt = self.first_paragraph()
        meta_guidance_type = soup.find("meta", {"name": "guidance_type"})
        if meta_guidance_type:
            super(AbstractGithubPage, self).save(*args, **kwargs)
            guidance_types = meta_guidance_type["content"].split(",")
            for guidance_type in guidance_types:
                StandardGuidanceTypes.objects.create(page=self, guidance_type=guidance_type.strip())

        self.ssot_root_slug = self.ssot_path.split("/")[0]
        super(AbstractGithubPage, self).save(*args, **kwargs)


class ActivityStandardPage(AbstractGithubPage):
    """A model for the Activity Standard Page, an IATI reference page."""

    template = 'iati_standard/activity_standard_page.html'


class StandardGuidancePage(AbstractGithubPage):
    """A model for the Standard Guidance Page, an IATI reference page."""

    template = 'iati_standard/standard_guidance_page.html'

    search_fields = AbstractGithubPage.search_fields + [
        FilterField('title'),
        FilterField('title_en')
    ]

    @cached_property
    def github_url(self):
        """Calculate a Github changelog url."""
        base_url = "https://github.com/IATI/IATI-Guidance/commits/master/en/"
        file_path = "/".join(self.ssot_path.split("/")[1:]) + ".rst"
        return base_url + file_path

    @cached_property
    def related_guidance(self):
        """Extract related_guidance."""
        related = []
        soup = BeautifulSoup(self.data, 'html.parser')
        anchors = soup.findAll("a")
        for anchor in anchors:
            anchor_href = anchor['href']
            anchor_ssot_path = os.path.relpath(os.path.join(self.ssot_path, anchor_href))
            anchor_match = StandardGuidancePage.objects.filter(ssot_path=anchor_ssot_path).first()
            if anchor_match and anchor_match not in related:
                related.append(anchor_match)
        return related


@register_snippet
class ReferenceMenu(models.Model):
    """A model for to store the Standard Reference menu."""

    def __str__(self):
        """Display the category name in the CMS rather than the class."""
        return self.menu_type + " - " + self.tag

    class Meta(object):
        """Change verbose name for correct pluralization."""

        verbose_name_plural = "reference menus"

    tag = models.CharField(
        max_length=255,
        help_text='Associated git release tag',
    )
    menu_type = models.CharField(
        default="ssot",
        max_length=255,
        help_text="The set of pages to which this menu belongs",
    )

    menu_json = JSONField()

    panels = [FieldPanel('menu_json', widget=JSONFieldWidget)]
