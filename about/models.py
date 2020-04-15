"""Model definitions for the about app."""

from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.blocks import CharBlock, StreamBlock, StructBlock, TextBlock
from wagtail.core.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel

from home.models import AbstractContentPage, AbstractIndexPage, DefaultPageHeaderImageMixin, PullQuoteBlock


class AboutPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """A model for the About landing page."""

    parent_page_types = ['home.HomePage']
    subpage_types = [
        'about.AboutSubPage',
        'about.CaseStudyIndexPage',
        'about.HistoryPage',
        'about.PeoplePage',
    ]

    max_count = 1

    show_featured_events = models.BooleanField(default=False)

    multilingual_field_panels = DefaultPageHeaderImageMixin.multilingual_field_panels + [
        FieldPanel('show_featured_events'),
    ]


class AboutSubPage(AbstractContentPage):
    """A model for generic About subpages."""

    parent_page_types = [
        'home.HomePage',
        'about.AboutPage',
        'about.AboutSubPage',
        'about.PeoplePage',
        'get_involved.GetInvolvedPage',
        'using_data.UsingDataPage',
    ]
    subpage_types = [
        'about.AboutSubPage',
        'about.PeoplePage',
        'governance.MembersAssemblyPage'
    ]

    show_featured_events = models.BooleanField(default=False)

    multilingual_field_panels = [
        FieldPanel('show_featured_events'),
    ]


class CaseStudyIndexPage(DefaultPageHeaderImageMixin, AbstractIndexPage):
    """A model for the Case Studies Index page."""

    parent_page_types = ['about.AboutPage']
    subpage_types = ['about.CaseStudyPage']

    max_count = 1

    show_featured_events = models.BooleanField(default=False)

    @property
    def case_studies(self):
        """Get all CaseStudyPage objects that have been published."""
        case_studies = CaseStudyPage.objects.child_of(self).live()
        return case_studies

    def get_context(self, request, *args, **kwargs):
        """Overwrite the default wagtail get_context function to allow for pagination.

        Use the functions built into the abstract index page class to apply pagination, limiting the results to 3 per page.

        """
        children = self.case_studies
        paginated_children = self.paginate(request, children, max_results=3)
        context = super(CaseStudyIndexPage, self).get_context(request)
        context['case_studies'] = paginated_children
        context['paginator_range'] = self._get_paginator_range(paginated_children)
        return context

    multilingual_field_panels = DefaultPageHeaderImageMixin.multilingual_field_panels + [
        FieldPanel('show_featured_events'),
    ]


class CaseStudyPage(AbstractContentPage):
    """A model for Case Study pages."""

    parent_page_types = ['about.CaseStudyIndexPage']
    subpage_types = []

    feed_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+',
        help_text='This is the image that will be displayed for the case study in the page header and on the Case Studies list page.'
    )

    multilingual_field_panels = [
        ImageChooserPanel('feed_image'),
    ]


class HistoryDateBlock(StreamBlock):
    """A block for History event card along the timeline which is shown on the HistoryPage."""

    event_block_editor = StructBlock([
        ('heading', CharBlock(required=False, max_length=100)),
        ('description', TextBlock(required=False))
    ])


class HistoryPage(AbstractContentPage):
    """A model for the History page."""

    parent_page_types = ['about.AboutPage']
    subpage_types = []

    max_count = 1

    timeline_editor = StreamField(HistoryDateBlock, null=True, blank=True)

    show_featured_events = models.BooleanField(default=False)

    translation_fields = AbstractContentPage.translation_fields + ['timeline_editor']

    multilingual_field_panels = [
        FieldPanel('show_featured_events'),
    ]


class PeopleProfileBlock(StreamBlock):
    """A block for People profiles."""

    section_heading = CharBlock(icon="title", classname="title")
    paragraph = CharBlock(icon="pilcrow")
    pullquote = PullQuoteBlock()
    profile_editor = StructBlock([
        ('name', CharBlock(required=False, max_length=100)),
        ('profile_picture', ImageChooserBlock(required=False, label="Profile picture", icon="image")),
        ('organisation_logo', ImageChooserBlock(required=False, label="Organisation logo", icon="image")),
        ('organisation_name', CharBlock(required=False, max_length=100)),
        ('IATI_role', CharBlock(required=False, max_length=100)),
        ('external_role', CharBlock(required=False, max_length=200)),
        ('description', TextBlock(required=False)),
        ('IATI_constituency', CharBlock(required=False, max_length=200))
    ], icon="image")


class PeoplePage(AbstractContentPage):
    """A model for the People page."""

    parent_page_types = [
        'about.AboutSubPage',
        'about.PeoplePage',
    ]
    subpage_types = [
        'about.AboutSubPage',
        'about.PeoplePage',
    ]

    profile_content_editor = StreamField(PeopleProfileBlock, null=True, blank=True)

    show_featured_events = models.BooleanField(default=False)

    translation_fields = AbstractContentPage.translation_fields + ['profile_content_editor']

    multilingual_field_panels = [
        FieldPanel('show_featured_events'),
    ]
