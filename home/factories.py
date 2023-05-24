import factory
from wagtail_factories import PageFactory
from django.utils.text import slugify
from wagtail.models import Page


class BasePageFactory(PageFactory):
    """Factory generating data for all Page models."""

    class Meta:
        model = Page
        abstract = True

    title = factory.Faker(
        'sentence',
        nb_words=4,
    )
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    url_path = factory.LazyAttribute(lambda n: "/%s/" % n)

    heading = factory.Faker(
        'sentence',
    )
    excerpt = factory.Faker(
        'paragraph',
    )
