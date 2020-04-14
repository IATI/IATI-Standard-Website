import factory
from factory import fuzzy
from wagtail_factories import ImageFactory
from django.utils import timezone
from django.utils.text import slugify
from home.factories import BasePageFactory
from news.models import (
    NewsCategory,
    NewsIndexPage,
    NewsPage,
    RelatedNews,
)


class NewsIndexPageFactory(BasePageFactory):
    """Factory generating data for NewsIndexPage."""

    class Meta:
        model = NewsIndexPage


class NewsPageFactory(BasePageFactory):
    """Factory generating data for NewsPage."""

    class Meta:
        model = NewsPage

    date = fuzzy.FuzzyDate(
        start_date=timezone.now() - timezone.timedelta(weeks=520),
        end_date=timezone.now(),
    )
    feed_image = factory.SubFactory(ImageFactory)

    @factory.post_generation
    def news_categories(self, create, categories, **kwargs):
        """Generate M2M for news categories."""
        if not create:
            return

        if categories:
            for category in categories:
                self.news_categories.add(category)

    @factory.post_generation
    def related_news(self, create, articles, **kwargs):
        """Generate M2M for related news."""
        if not create:
            return

        if articles:
            for article in articles:
                self.related_news.add(article)


class NewsCategoryFactory(factory.django.DjangoModelFactory):
    """Factory generating data for NewsCategory snippet."""

    class Meta:
        model = NewsCategory

    name = factory.Faker(
        'sentence',
        nb_words=2,
    )
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


class RelatedNewsFactory(factory.django.DjangoModelFactory):
    """Factory generating data for RelatedNews snippet."""

    class Meta:
        model = RelatedNews

    related_post = factory.SubFactory(NewsPageFactory)
