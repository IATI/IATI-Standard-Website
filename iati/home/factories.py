import factory
from factory.fuzzy import FuzzyInteger
from wagtail_factories import PageFactory
from django.utils.text import slugify
from wagtail.core.models import Page
from home.models import HomePage


class InPageFactory(PageFactory):

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


class BasePageFactory(InPageFactory):

    class Meta:
        model = Page
        abstract = True

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


class HomePageFactory(BasePageFactory):
    """Factory with fake data for HomePage."""

    class Meta:
        model = HomePage
        django_get_or_create = ('title', 'path',)

    title = 'Home'
    path = '00010001'
    activities = FuzzyInteger(1000000, 1500000)
    organisations = FuzzyInteger(700, 900)
