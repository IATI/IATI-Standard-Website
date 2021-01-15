import pytest
from django.core.management import call_command
from common.tasks import multiplication_test
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


@pytest.fixture
def task_result(django_db_blocker):
    with django_db_blocker.unblock():
        task_result = multiplication_test.delay(4, 4).get(timeout=10) == 16
    return task_result



class TestServices():
    """Tests Celery, Rabbit, and ElasticSearch services via updating index."""

    @pytest.mark.timeout(10)
    def test_run_task(self, task_result):
        """Run a test task."""
        assert task_result

    @pytest.mark.django_db
    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_event_search(self, client, es_events):
        """Test that event with random date is created."""
        search_results = EventPage.objects.search(EventPage.objects.first().title).annotate_score("_score")
        search_scores = [page._score for page in search_results]
        assert sum(search_scores) > 0
