import pytest
from django.utils import timezone
from events.factories import EventPageFactory, EventIndexPageFactory, EventTypeFactory
from events.models import EventPage
from home.models import HomePage


@pytest.fixture
def events():
    """Fixture to generate event pages."""
    home_page = HomePage.objects.first()
    event_listing = EventIndexPageFactory(
        parent=home_page
    )
    event_types = EventTypeFactory.create_batch(2)
    EventPageFactory.create_batch(
        4,
        parent=event_listing,
        event_type=[event_types[0]],
        starts_in_past=True,
    )
    EventPageFactory.create_batch(
        4,
        parent=event_listing,
        event_type=[event_types[1]],
        starts_in_future=True
    )
    return event_listing


@pytest.mark.django_db
class TestEventPage():
    """Tests EventPage."""

    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_event_types_on_index(self, client, events):
        """Test that event with random date is created."""
        assert events.event_types.count() == 2

    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_past_events(self, client, events):
        """Test that past parameter calls past events."""
        response = client.get(events.url, {'past': 1}, follow=True)
        today_end_date = timezone.datetime.combine(timezone.now(), timezone.datetime.min.time())
        events_before_now = EventPage.objects.filter(date_end__lt=today_end_date).values_list('id', flat=True)
        events_in_response = response.context['events'].paginator.object_list.values_list('id', flat=True)
        assert set(events_before_now) == set(events_in_response)
        assert response.context['past'] == 1

    # def test_past_event_image_resolves(self, client):
    #     """Test that image resolves."""
    #     event_listing = EventIndexPageFactory(parent=self.home_page)
    #     feed_image = ImageFactory(file__filename='event_test.jpg')
    #     past_event = EventPageFactory.create(
    #         parent=event_listing,
    #         starts_in_past=True,
    #         feed_image=feed_image
    #     )
    #     response = generate_image_url(past_event.feed_image, 'original')
    #     image_via_url = client.get(response, follow=True)
    #     assert image_via_url.status_code == 200
