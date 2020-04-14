import pytest
from news.factories import (
    NewsIndexPageFactory,
    NewsPageFactory,
    NewsCategoryFactory,
)
from home.models import HomePage


@pytest.mark.django_db
class TestNewsPage():
    """Tests EventPage."""

    @property
    def home_page(self):
        """Return HomePage created in migrations."""
        return HomePage.objects.first()

    def test_guidance_tree(self, client):
        """Test that event with random date is created."""
        news_index = NewsIndexPageFactory.create()
        NewsCategoryFactory.create_batch(4)
        NewsPageFactory.create_batch(4, parent=news_index)

        assert news_index is not None
