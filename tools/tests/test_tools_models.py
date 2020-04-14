import pytest
from tools.factories import ToolsListingPageFactory, ToolPageFactory
from home.models import HomePage


def listing():
    """Fixture to generate tools pages."""
    home_page = HomePage.objects.first()
    listing = ToolsListingPageFactory(
        parent=home_page
    )
    ToolPageFactory.create_batch(
        4,
        parent=listing,
    )
    # listing.featured_tool(True, tools=tools[:5])
    return listing


@pytest.fixture(name="listing")
def listing_fixture():
    return listing()


@pytest.mark.django_db
class TestTools():
    """Tests EventPage."""

    @property
    def home_page(self):
        """Return HomePage created in migrations."""
        return HomePage.objects.first()

    def test_listing(self, client):
        """Test that listing page is created."""

        assert listing() is not None

    def test_tools(self, client):
        """Test that listing page has children ."""

        assert listing().get_children().count() == 4

    # def test_featured_tools(self, client):
    #     """Test that listing page has featured tools."""

    #     assert listing().tools().count() == 5
