from factory.fuzzy import FuzzyInteger
from wagtail_factories import PageFactory
from home.models import HomePage


class HomePageFactory(PageFactory):
    """Factory with fuzzy data for HomePage."""

    class Meta:
        model = HomePage

    activities = FuzzyInteger(1000000, 1500000)
    organisations = FuzzyInteger(700, 900)
