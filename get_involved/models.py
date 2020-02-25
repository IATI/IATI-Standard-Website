"""Model definitions for the get involved app."""
from wagtail.admin.edit_handlers import InlinePanel
from home.models import AbstractContentPage, DefaultPageHeaderImageMixin, highlight_streamfield
from get_involved.inlines import *  # noqa


class GetInvolvedPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """A model for get involved page, the get involved landing page."""

    parent_page_types = ['home.HomePage']
    subpage_types = ['about.AboutSubPage']

    highlight = highlight_streamfield()

    translation_fields = AbstractContentPage.translation_fields + [
        'highlight',
    ]

    multilingual_field_panels = DefaultPageHeaderImageMixin.multilingual_field_panels + [
        InlinePanel(
            'get_involved_items',
            heading='Get involved items',
            label='Get involved item',
        ),
    ]
