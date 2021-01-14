import pytest
from django.core.management import call_command
from events.factories import EventPageFactory, EventIndexPageFactory, EventTypeFactory
from events.models import EventPage
from home.models import HomePage


@pytest.fixture
def es_events():
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
    call_command('update_index', verbosity=0)
    return event_listing


@pytest.mark.django_db
class TestServices():
    """Tests ElasticSearch via updating index."""

    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_event_search(self, client, es_events):
        """Test that event with random date is created."""
        search_results = EventPage.objects.search(EventPage.objects.first().title).annotate_score("_score")
        search_scores = [page._score for page in search_results]
        assert sum(search_scores) > 0

    def test_create_task(self, celery_app, celery_worker):
        @celery_app.task
        def mul(x, y):
            return x * y

        celery_worker.reload()

        assert mul.delay(4, 4).get(timeout=10) == 16
