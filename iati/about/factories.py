import factory
from about.models import CaseStudyPage, CaseStudyIndexPage
from home.factories import BasePageFactory


class CaseStudyPageFactory(BasePageFactory):
    """Factory with fake data for CaseStudyPage."""

    class Meta:
        model = CaseStudyPage
        django_get_or_create = ('title', 'path',)


class CaseStudyIndexPageFactory(BasePageFactory):
    """Factory with fake data for CaseStudyIndexPage."""

    class Meta:
        model = CaseStudyIndexPage
        django_get_or_create = ('title', 'path',)
