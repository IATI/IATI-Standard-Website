from django.db import models

from home.models import AbstractContentPage, AbstractIndexPage


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
