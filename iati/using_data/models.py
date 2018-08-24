"""Model definitions for the using_data app."""

from about.models import AboutPage, AboutSubPage


class UsingDataPage(AboutPage):
    """A page model for the Using IATI data page. Inherits all from AboutPage."""

    subpage_types = ['using_data.ToolsIndexPage', 'about.AboutSubPage']


class ToolsIndexPage(AboutSubPage):
    """A page model for the Tools & Resources page. Inherits all from AboutSubPage."""

    parent_page_types = ['using_data.UsingDataPage']
    subpage_types = ['using_data.ToolsPage']


class ToolsPage(AboutSubPage):
    """A page model for single Tools & Resources pages. Inherits all form AboutSubPage."""

    parent_page_types = ['using_data.ToolsIndexPage']
