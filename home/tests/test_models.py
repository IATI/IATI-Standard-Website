import pytest
from about.factories import CaseStudyPageFactory, CaseStudyIndexPageFactory
from home.models import HomePage


@pytest.mark.django_db
class TestHomePage():
    """Tests for Home Page."""

    @property
    def home_page(self):
        """Return HomePage created in migrations."""
        return HomePage.objects.first()

    def test_home_page_lists_all_case_studies(self, client):
        """Test that the homepage title is as set by the factory."""
        case_study_index = CaseStudyIndexPageFactory(
            title='Case Studies',
            parent=self.home_page
        )
        case_study_pages = CaseStudyPageFactory.create_batch(
            size=4,
            parent=case_study_index
        )

        home_page_context = client.get(self.home_page.url, follow=True).context
        home_page_case_studies = home_page_context.get('case_studies', None)

        assert len(case_study_pages) == len(home_page_case_studies)

    def test_home_page_lists_live_case_studies(self, client):
        """Test that the homepage title is as set by the factory."""
        case_study_index = CaseStudyIndexPageFactory(
            title='Case Studies',
            parent=self.home_page
        )
        CaseStudyPageFactory.create_batch(
            size=4,
            parent=case_study_index,
            live=False,
        )

        home_page_context = client.get(self.home_page.url, follow=True).context
        home_page_case_studies = home_page_context.get('case_studies', None)

        assert len(home_page_case_studies) == 0
