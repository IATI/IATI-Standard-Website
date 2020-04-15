import pytest
from home.models import HomePage


@pytest.mark.django_db
class TestHomePage():
    """Tests for Home Page."""

    @property
    def home_page(self):
        """Return HomePage created in migrations."""
        return HomePage.objects.first()
