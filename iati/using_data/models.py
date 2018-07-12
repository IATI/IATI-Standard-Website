from about.models import AboutPage


class UsingDataPage(AboutPage):  # pylint: disable=too-many-ancestors
    """A page model for the Using IATI data page. Inherits all from AboutPage."""

    template = 'about/about_page.html'
