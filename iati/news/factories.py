import factory
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

    class Meta:
        model = NewsIndexPage


class NewsPageFactory(BasePageFactory):

    class Meta:
        model = NewsPage

    date = factory.fuzzy.FuzzyDate(
        start_date=timezone.now() - timezone.timedelta(weeks=520),
        end_date=timezone.now(),
    )
    feed_image = factory.SubFactory(ImageFactory)

    @factory.post_generation
    def news_categories(self, create, categories, **kwargs):
        """Factory for multiple event types."""
        if not create:
            return

        if categories:
            for category in categories:
                self.news_categories.add(category)

    @factory.post_generation
    def related_news(self, create, articles, **kwargs):
        """Factory for multiple event types."""
        if not create:
            return

        if articles:
            for article in articles:
                self.related_news.add(article)


class NewsCategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = NewsCategory

    name = factory.Faker(
        'sentence',
        nb_words=2,
    )
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


class RelatedNewsFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = RelatedNews

    related_post = factory.SubFactory(NewsPageFactory)
