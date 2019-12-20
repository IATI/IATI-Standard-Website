import factory
from wagtail_factories import ImageFactory
from tools.models import ToolsListingPage, ToolPage, FeaturedTool
from home.factories import BasePageFactory


class ToolsListingPageFactory(BasePageFactory):
    """Factory generating data for ToolsListingPage."""

    class Meta:
        model = ToolsListingPage
        django_get_or_create = ('title', 'path',)

    @factory.post_generation
    def featured_tool(self, create, tools, **kwargs):
        """Generate M2M for related news."""
        if not create:
            return

        if tools:
            for tool in tools:
                self.featured_tools.add(tool)


class ToolPageFactory(BasePageFactory):
    """Factory generating data for EventPage."""

    class Meta:
        model = ToolPage
        django_get_or_create = ('title', 'path',)

    external_url = factory.Faker(
        provider='uri',
    )
    listing_description = factory.Faker('listing_description')
    logo = factory.SubFactory(ImageFactory)
    button_label = factory.Faker('button_label')


class FeaturedToolsFactory(factory.django.DjangoModelFactory):
    """Factory generating data for featured_tools inline panel."""

    class Meta:
        model = FeaturedTool

    tool = factory.SubFactory(ToolsListingPageFactory)
