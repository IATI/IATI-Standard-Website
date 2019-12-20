import pytest
from tools.factories import ToolsListingPageFactory, ToolPageFactory, FeaturedToolsFactory
from home.models import HomePage


@pytest.fixture
def listing():
    """Fixture to generate tools pages."""
    home_page = HomePage.objects.first()
    listing = ToolsListingPageFactory(
        parent=home_page
    )
    ToolPageFactory.create_batch(
        10,
        parent=listing,
    )
    return listing


@pytest.mark.django_db
class TestTools():
    """Tests EventPage."""

    @property
    def home_page(self):
        """Return HomePage created in migrations."""
        return HomePage.objects.first()

    def test_listing(self, client):
        """Test that listing page is created."""

        assert listing().listing is not None

    def test_tools(self, client):
        """Test that listing page is created."""

        assert listing.children().count() == 10
