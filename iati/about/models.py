from django.db import models

from wagtail.core.models import Orderable
from wagtail.documents.edit_handlers import DocumentChooserPanel

from modelcluster.fields import ParentalKey
from home.models import AbstractContentPage, AbstractIndexPage


class AboutPage(AbstractContentPage):
    """A model for the About landing page."""
    parent_page_types = ['home.HomePage']
    subpage_types = ['about.AboutSubPage', 'about.CaseStudyIndexPage']


class AboutSubPage(AbstractContentPage):
    """A model for generic About subpages."""
    parent_page_types = ['about.AboutPage']
    subpage_types = []


class CaseStudyIndexPage(AbstractIndexPage):
    """"A model for the Case Studies Index page."""
    parent_page_types = ['about.AboutPage']
    subpage_types = ['about.CaseStudyPage']

    @property
    def case_studies(self):
        """Get all CaseStudyPage objects that have been published."""
        case_studies = CaseStudyPage.objects.child_of(self).live()
        return case_studies

    def get_context(self, request):
        """Overwriting the default wagtail get_context function to allow for pagination.

        Use the functions built into the abstract index page class to apply pagination, limiting the results to 3 per page.

        """
        children = self.case_studies
        paginated_children = self.paginate(request, children, 3)
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
        related_name='+'
    )


class CaseStudyDocument(Orderable):
    page = ParentalKey(CaseStudyPage, related_name='case_study_documents')
    document = models.ForeignKey(
        'wagtaildocs.Document',
        on_delete=models.CASCADE,
        related_name='+'
    )
    panels = [
        DocumentChooserPanel('document'),
    ]
