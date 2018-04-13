from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from home.models import IATIStreamBlock


class AbstractContentPage(Page):
    """
    TODO:
        Remove this once add-abstract-page-models is merged.

    """
    heading = models.CharField(max_length=255, null=True, blank=True)
    excerpt = models.TextField(null=True, blank=True)
    content_editor = StreamField(IATIStreamBlock(required=False), null=True, blank=True)

    class Meta:
        abstract = True


class AbstractIndexPage(Page):
    """
    TODO:
        Remove this once add-abstract-page-models is merged.

    """
    heading = models.CharField(max_length=255, null=True, blank=True)
    excerpt = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class AboutPage(AbstractContentPage):
    """A model for the About landing page."""
    parent_page_types = ['home.HomePage']
    subpage_types = ['about.AboutSubPage']


class AboutSubPage(AbstractContentPage):
    """A model for generic About subpages."""
    parent_page_types = ['about.AboutPage']
    subpage_types = []


class CaseStudiesIndexPage(AbstractIndexPage):
    """"A model for the Case Studies Index page."""
    parent_page_types = ['about.AboutPage']
    subpage_types = ['about.CaseStudyPage']

    @property
    def case_studies(self):
        """Get all CaseStudyPage objects that have been published."""
        case_studies = CaseStudyPage.objects.child_of(self).live()
        return case_studies


class CaseStudyPage(AbstractContentPage):
    """A model for Case Study pages."""
    parent_page_types = ['about.CaseStudiesIndexPage']
    subpage_types = []
