import factory
from wagtail_factories import PageFactory
from django.utils.text import slugify
from wagtail.core.models import Page


class BasePageFactory(PageFactory):
    """Factory generating data for all Page models."""

    class Meta:
        model = Page
        abstract = True

    title = factory.Faker(
        'sentence',
        nb_words=4,
    )
    title_fr = factory.Faker(
        'sentence',
        locale='fr_FR',
        nb_words=4,
    )
    slug_fr = factory.LazyAttribute(lambda obj: slugify(obj.title_fr))
    url_path_fr = factory.LazyAttribute(lambda n: "/%s/" % n)

    heading = factory.Faker(
        'sentence',
    )
    heading_fr = factory.Faker(
        'sentence',
        locale='fr_FR',
        nb_words=6,
    )
    excerpt = factory.Faker(
        'paragraph',
    )
    excerpt_fr = factory.Faker(
        'paragraph',
        locale='fr_FR',
    )
