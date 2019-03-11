import pytest
from events.factories import EventPageFactory
from home.models import HomePage


@pytest.mark.django_db
class TestEventPage():

    @property
    def home_page(self):
        """Return HomePage created in migrations."""
        return HomePage.objects.first()

    def test_random_event(self, client):
        random_event = EventPageFactory()
        assert random_event is not None

    def test_future_event(self, client):
        future_event = EventPageFactory(
            starts_in_future=True
        )
        assert future_event is not None

    def test_past_event(self, client):
        past_event = EventPageFactory(
            starts_in_past=True
        )
        import pdb; pdb.set_trace()
        assert past_event is not None
