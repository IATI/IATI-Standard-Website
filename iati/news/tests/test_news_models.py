import pytest
import random
from news.factories import (
    NewsIndexPageFactory,
    NewsPageFactory,
    NewsCategoryFactory,
    RelatedNewsFactory,
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
        NewsCategoryFactory.create_batch(10)
        NewsPageFactory.create_batch(10, parent=news_index)

        assert news_index is not None
