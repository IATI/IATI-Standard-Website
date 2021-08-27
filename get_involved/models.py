"""Model definitions for the get involved app."""
from django.utils.functional import cached_property
from wagtail.admin.edit_handlers import InlinePanel, StreamFieldPanel
from home.models import AbstractContentPage, DefaultPageHeaderImageMixin, highlight_streamfield
from get_involved.inlines import *  # noqa


class GetInvolvedPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """A model for get involved page, the get involved landing page."""

    parent_page_types = ['home.HomePage']
    subpage_types = ['about.AboutSubPage']

    max_count = 1

    highlight = highlight_streamfield()

    content_panels =  AbstractContentPage.content_panels + DefaultPageHeaderImageMixin.content_panels + [
        InlinePanel(
            'get_involved_items',
            heading='Get involved items',
            label='Get involved item',
        ),
        StreamFieldPanel('highlight')
    ]

    @cached_property
    def get_involved(self):
        """Create and return a list of get_involved items, added to list if no page or the page is live."""
        return [x for x in self.get_involved_items.all() if not x.page or x.page.live]
