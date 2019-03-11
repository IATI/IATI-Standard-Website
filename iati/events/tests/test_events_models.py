import pytest
from events.factories import EventPageFactory, EventIndexPageFactory
from home.models import HomePage


@pytest.mark.django_db
class TestEventPage():

    @property
    def home_page(self):
        """Return HomePage created in migrations."""
        return HomePage.objects.first()

    def test_random_event(self, client):
        event_listing = EventIndexPageFactory()
        random_event = EventPageFactory(parent=event_listing)
        assert random_event is not None

    def test_future_event(self, client):
        event_listing = EventIndexPageFactory()
        future_event = EventPageFactory(
            parent=event_listing,
            starts_in_future=True
        )
        assert future_event is not None

    def test_past_event(self, client):
        event_listing = EventIndexPageFactory()
        past_event = EventPageFactory(
            parent=event_listing,
            starts_in_past=True
        )
        assert past_event is not None
