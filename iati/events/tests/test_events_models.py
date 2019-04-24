import pytest
from django.utils import timezone
from wagtail_factories import ImageFactory
from events.factories import EventPageFactory, EventIndexPageFactory, EventTypeFactory
from events.models import EventPage
from home.models import HomePage
from home.utils import generate_image_url


@pytest.fixture
def events():
    """Fixture to generate event pages."""
    home_page = HomePage.objects.first()
    event_listing = EventIndexPageFactory(
        parent=home_page
    )
    event_types = EventTypeFactory.create_batch(2)
    EventPageFactory.create_batch(
        10,
        parent=event_listing,
        event_type=[event_types[0]],
        starts_in_past=True,
    )
    EventPageFactory.create_batch(
        10,
        parent=event_listing,
        event_type=[event_types[1]],
        starts_in_future=True
    )
    return event_listing


@pytest.mark.django_db
class TestEventPage():
    """Tests EventPage."""

    def test_event_types_on_index(self, client, events):
        """Test that event with random date is created."""
        assert events.event_types.count() == 2

    def test_past_events(self, client, events):
        """Test that past parameter calls past events."""
        response = client.get(events.url, {'past': 1}, follow=True)
        events_before_now = EventPage.objects.filter(date_start__lte=timezone.now()).values_list('id', flat=True)
        events_in_response = response.context['events'].paginator.object_list.values_list('id', flat=True)
        assert set(events_before_now) == set(events_in_response)
        assert response.context['past'] == 1

    def test_events_in_future(self, client, events):
        """Test that lack of past parameter returns future events."""
        response = client.get(events.url, follow=True)
        events_in_future = EventPage.objects.filter(date_start__gte=timezone.now()).values_list('id', flat=True)
        events_in_response = response.context['events'].paginator.object_list.values_list('id', flat=True)
        assert set(events_in_future) == set(events_in_response)
        assert not response.context['past']
