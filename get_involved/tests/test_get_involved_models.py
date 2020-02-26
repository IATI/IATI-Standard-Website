import pytest
from get_involved.factories import GetInvolvedPageFactory
from home.models import HomePage


def get_involved():
    """Fixture to generate get involved pages."""
    home_page = HomePage.objects.first()
    page = GetInvolvedPageFactory(
        parent=home_page
    )
    return page


@pytest.mark.django_db
class TestGetInvolved():
    """Tests GetInvolvedPage."""

    def test_get_involved(self, client):
        """Test that get involved page is created."""

        assert get_involved() is not None
