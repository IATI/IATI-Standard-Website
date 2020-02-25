"""Model definitions for the get involved app."""
from wagtail.admin.edit_handlers import InlinePanel, MultiFieldPanel
from home.models import AbstractContentPage, DefaultPageHeaderImageMixin, highlight_streamfield


class GetInvolvedPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """A model for get involved page, the get involved landing page."""

    parent_page_types = ['home.HomePage']
    subpage_types = ['about.AboutSubPage']

    highlight = highlight_streamfield()

    translation_fields = AbstractContentPage.translation_fields + [
        'highlight',
    ]

    multilingual_field_panels = DefaultPageHeaderImageMixin.multilingual_field_panels + [
        MultiFieldPanel(
            [
                InlinePanel('get_involved_items', label='Get involved item', help_text='Add get involved items with optional images and page links.'),
            ],
            heading='Get involved items',
        )
    ]
