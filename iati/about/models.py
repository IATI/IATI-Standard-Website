from django.db import models

from wagtail.admin.edit_handlers import InlinePanel
from wagtail.core.blocks import CharBlock, StreamBlock, StructBlock, TextBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, Page
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from modelcluster.fields import ParentalKey
from home.models import AbstractContentPage, AbstractIndexPage, IATIStreamBlock


class AboutPage(AbstractContentPage):
    """A model for the About landing page."""

    parent_page_types = ['home.HomePage']
    subpage_types = ['about.AboutSubPage', 'about.CaseStudyIndexPage', 'about.HistoryPage', 'about.PeoplePage']

    def save(self, *args, **kwargs):
        """Create a menu item snippet on save"""
        super(AboutPage, self).save(*args, **kwargs)
        try:
            menu_item = AboutMenuItems.objects.get(page=self)
        except AboutMenuItems.DoesNotExist:
            menu_item = AboutMenuItems(page=self, order=self.pk)
            menu_item.save()


class AboutSubPage(AbstractContentPage):
    """A model for generic About subpages."""

    subpage_types = ['about.AboutSubPage', 'about.PeoplePage']

    multilingual_field_panels = [
        InlinePanel('about_sub_page_documents', label='About subpage attachments'),
    ]


class AboutSubPageDocument(Orderable):
    """A model for About sub page documents."""

    page = ParentalKey(AboutSubPage, related_name='about_sub_page_documents')
    document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        DocumentChooserPanel('document'),
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
        paginated_children = self.paginate(request, children, max_results=3)
        context = super(CaseStudyIndexPage, self).get_context(request)
        context['case_studies'] = paginated_children
        return context


class CaseStudyPage(AbstractContentPage):
    """A model for Case Study pages."""

    parent_page_types = ['about.CaseStudyIndexPage']
    subpage_types = []

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='This is the image that will be displayed for the case study on the Case Studies list page.'
    )

    multilingual_field_panels = [
        ImageChooserPanel('feed_image'),
        InlinePanel('case_study_documents', label='Case study attachments'),
    ]


class CaseStudyDocument(Orderable):
    """A model for Case Study documents."""

    page = ParentalKey(CaseStudyPage, related_name='case_study_documents')
    document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    panels = [
        DocumentChooserPanel('document'),
    ]


class HistoryDateBlock(StreamBlock):
    """A block for History event card along the timeline which is shown on the HistoryPage."""

    event_block_editor = StructBlock([
        ('heading', CharBlock(required=False, max_length=100)),
        ('description', TextBlock(required=False))
    ])


class HistoryPage(AbstractContentPage):
    """A model for the History page."""

    subpage_types = []

    timeline_editor = StreamField(HistoryDateBlock, null=True, blank=True)

    translation_fields = AbstractContentPage.translation_fields + ['date_panel']


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

    translation_fields = AbstractContentPage.translation_fields + ['subheading', 'profile_panel']


@register_snippet
class AboutMenuItems(models.Model):
    page = models.OneToOneField(
        Page,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    order = models.IntegerField()
