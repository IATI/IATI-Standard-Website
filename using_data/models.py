"""Model definitions for the using_data app."""

from about.models import AboutSubPage, AboutPage
from tools.models import ToolsListingPage


class UsingDataPage(AboutPage):
    """A page model for the Using IATI data page. Inherits all from AboutPage."""

    parent_page_types = ['home.HomePage']
    subpage_types = ['about.AboutSubPage']

    max_count = 1

    def get_context(self, request, *args, **kwargs):
        """Overwrite the default wagtail get_context function to add all subpages of UsingDataPage."""
        context = super(UsingDataPage, self).get_context(request)

        context['subpages'] = AboutSubPage.objects.child_of(self)
        context['toolsindex'] = ToolsListingPage.objects.all().first()
        return context
