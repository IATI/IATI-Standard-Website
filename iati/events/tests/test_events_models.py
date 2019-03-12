import pytest
from wagtail_factories import ImageFactory
from events.factories import EventPageFactory, EventIndexPageFactory
from home.models import HomePage
from home.utils import generate_image_url


@pytest.mark.django_db
class TestEventPage():
    """Tests EventPage."""

    @property
    def home_page(self):
        """Return HomePage created in migrations."""
        return HomePage.objects.first()

    def test_random_event(self, client):
        """Test that event with random date is created."""
        event_listing = EventIndexPageFactory(parent=self.home_page)
        random_event = EventPageFactory(parent=event_listing)
        assert random_event is not None

    def test_future_event(self, client):
        """Test that future event is created."""
        event_listing = EventIndexPageFactory(parent=self.home_page)
        future_event = EventPageFactory(
            parent=event_listing,
            starts_in_future=True
        )
        assert future_event is not None

    def test_past_event_image_resolves(self, client):
        """Test that image resolves."""
        event_listing = EventIndexPageFactory(parent=self.home_page)
        feed_image = ImageFactory(file__filename='event_test.jpg')
        past_event = EventPageFactory.create(
            parent=event_listing,
            starts_in_past=True,
            feed_image=feed_image
        )
        response = generate_image_url(past_event.feed_image, 'original')
        image_via_url = client.get(response, follow=True)
        assert image_via_url.status_code == 200
