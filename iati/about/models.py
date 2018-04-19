from django.db import models

from wagtail.admin.edit_handlers import InlinePanel
from wagtail.core.blocks import CharBlock, StreamBlock, StructBlock, TextBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.blocks import ImageChooserBlock

from modelcluster.fields import ParentalKey
from home.models import AbstractContentPage, AbstractIndexPage, IATIStreamBlock


class AboutPage(AbstractContentPage):
    """A model for the About landing page."""

    parent_page_types = ['home.HomePage']
    subpage_types = ['about.AboutSubPage', 'about.CaseStudyIndexPage', 'about.HistoryPage', 'about.PeoplePage']

    translation_fields = [
        'heading',
        'excerpt',
        'content_editor'
    ]


class AboutSubPage(AbstractContentPage):
    """A model for generic About subpages."""

    subpage_types = ['about.AboutSubPage']

    translation_fields = [
        'heading',
        'excerpt',
        'content_editor'
    ]


class CaseStudyIndexPage(AbstractIndexPage):
    """A model for the Case Studies Index page."""

    subpage_types = ['about.CaseStudyPage']

    @property
    def case_studies(self):
        """Get all CaseStudyPage objects that have been published."""
        case_studies = CaseStudyPage.objects.child_of(self).live()
        return case_studies

    def get_context(self, request):
        """Overwrite the default wagtail get_context function to allow for pagination.

        Use the functions built into the abstract index page class to apply pagination, limiting the results to 3 per page.

        """
        children = self.case_studies
        paginated_children = self.paginate(request, children, 3)
        context = super(CaseStudyIndexPage, self).get_context(request)
        context['case_studies'] = paginated_children
        return context

    translation_fields = [
        'heading',
        'excerpt'
    ]


class CaseStudyPage(AbstractContentPage):
    """A model for Case Study pages."""

    parent_page_types = ['about.CaseStudyIndexPage']
    subpage_types = []

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    translation_fields = [
        'heading',
        'excerpt',
        'content_editor'
    ]

    multilingual_field_panels = [
        InlinePanel('case_study_documents', label='Case study attachments'),
    ]


class CaseStudyDocument(Orderable):
    """A model for Case Study documents."""

    page = ParentalKey(CaseStudyPage, related_name='case_study_documents')
    document = models.ForeignKey(
        'wagtaildocs.Document',
        on_delete=models.CASCADE,
        related_name='+'
    )
    panels = [
        DocumentChooserPanel('document'),
    ]


class HistoryDateBlock(StreamBlock):
    """A block for History page info."""

    date_block_editor = StructBlock([
        ('heading', CharBlock(required=False, max_length=100)),
        ('description', TextBlock(required=False))
    ])


class HistoryPage(AbstractContentPage):
    """A model for the History page."""

    subpage_types = []

    date_panel = StreamField(HistoryDateBlock, null=True, blank=True)

    translation_fields = [
        'heading',
        'excerpt',
        'content_editor',
        'date_panel'
    ]


class PeopleProfileBlock(StreamBlock):
    """A block for People profiles."""
    profile_editor = StructBlock([
        ('name', CharBlock(required=False, max_length=100)),
        ('profile_picture', ImageChooserBlock(required=False, label="Profile picture", icon="image")),
        ('organisation_logo', ImageChooserBlock(required=False, label="Organisation logo", icon="image")),
        ('IATI_role', CharBlock(required=False, max_length=100)),
        ('external_role', CharBlock(required=False, max_length=200)),
        ('description', TextBlock(required=False)),
        ('IATI_constituency', CharBlock(required=False, max_length=200))
    ])


class PeoplePage(AbstractContentPage):
    """A model for the People page."""

    subpage_types = []

    subheading = StreamField(IATIStreamBlock(required=False), null=True, blank=True)
    profile_panel = StreamField(PeopleProfileBlock, null=True, blank=True)

    translation_fields = [
        'heading',
        'excerpt',
        'content_editor',
        'subheading',
        'profile_panel'
    ]
