import factory
from factory.fuzzy import FuzzyChoice
from factory import fuzzy
import random
from wagtail_factories import ImageFactory
from django.utils import timezone
from django.utils.text import slugify
from events.models import EventIndexPage, EventPage, EventType, FeaturedEvent
from home.factories import BasePageFactory


class EventIndexPageFactory(BasePageFactory):
    """Factory generating data for EventIndexPage."""

    class Meta:
        model = EventIndexPage
        django_get_or_create = ('title', 'path',)


class EventPageFactory(BasePageFactory):
    """Factory generating data for EventPage."""

    class Meta:
        model = EventPage
        django_get_or_create = ('title', 'path',)

    featured_event = FuzzyChoice(
        choices=(True, False)
    )
    date_start = fuzzy.FuzzyDate(
        start_date=timezone.now() - timezone.timedelta(weeks=520),
        end_date=timezone.now() + timezone.timedelta(weeks=52),
    )
    date_end = factory.LazyAttribute(
        lambda o: o.date_start + timezone.timedelta(days=random.randint(0, 10))
    )
    location = factory.Faker(
        provider='city',
        locale='en_GB',
    )
    registration_link = factory.Faker(
        provider='uri',
    )
    feed_image = factory.SubFactory(ImageFactory)

    @factory.post_generation
    def event_type(self, create, events, **kwargs):
        """Generate M2M for event types."""
        if not create:
            return

        if events:
            for event in events:
                self.event_type.add(event)

    class Params:
        starts_in_future = factory.Trait(
            date_start=fuzzy.FuzzyDate(
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30),
            )
        )
        starts_in_past = factory.Trait(
            date_start=fuzzy.FuzzyDate(
                start_date=timezone.now() - timezone.timedelta(weeks=12),
                end_date=timezone.now() - timezone.timedelta(days=1),
            ),
        )


class EventTypeFactory(factory.django.DjangoModelFactory):
    """Factory generating data for EventType snippet."""

    class Meta:
        model = EventType

    name = factory.Faker(
        'word',
    )
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


class FeaturedEventFactory(factory.django.DjangoModelFactory):
    """Factory generating data for FeaturedEvent snippet."""

    class Meta:
        model = FeaturedEvent

    event = factory.SubFactory(EventPageFactory)
