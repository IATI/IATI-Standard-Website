import pytest
from about.factories import CaseStudyPageFactory, CaseStudyIndexPageFactory
from home.factories import HomePageFactory


@pytest.mark.django_db
def test_case_study_page(client):
    """Test that the Case Study page is created."""
    home_page = HomePageFactory(title='Home', path='00010001', parent=None)
    case_study_index = CaseStudyIndexPageFactory(
        title='Case Studies',
        parent=home_page
    )
    case_study_pages = CaseStudyPageFactory.create_batch(
        size=10,
        parent=case_study_index
    )
    assert case_study_pages[0].title is not None
