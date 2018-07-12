"""A module for the IATI Standard page model."""

from home.models import AbstractContentPage, DefaultPageHeaderImageMixin


class IATIStandardPage(DefaultPageHeaderImageMixin, AbstractContentPage):  # pylint: disable=too-many-ancestors
    """A model for the IATI Standard Page, a landing page for IATI reference."""

    parent_page_types = ['home.HomePage']
    subpage_types = []
