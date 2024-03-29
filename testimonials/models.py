from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from common.utils import WagtailImageField
from dashboard.edit_handlers import HelpPanel


@register_snippet
class Testimonial(index.Indexed, models.Model):
    """A snippet class for reusable testimonal items, with an optional image."""

    class Meta:
        verbose_name = 'Testimonial'
        ordering = ['quotee']

    quote = models.CharField(
        max_length=255,
        help_text='The quote for the testimonial',
    )
    quotee = models.TextField(
        help_text='The source of the quote',
    )
    image = WagtailImageField(
        required=False,
        help_text='Optional: image for the quotee'
    )

    translation_fields = [
        'quote',
        'quotee',
    ]

    search_fields = [
        index.SearchField('quote', partial_match=True),
        index.SearchField('quotee', partial_match=True),
    ]

    panels = [
        HelpPanel(
            content='Add a quote, quotee, and an optional image',
            wrapper_class='help-block help-block--snippet-initial help-info',
        ),
        FieldPanel('quote'),
        FieldPanel('quotee'),
        FieldPanel('image'),
    ]

    def __str__(self):
        """Get a string representation of the snippet, the quotee."""
        return self.quotee
