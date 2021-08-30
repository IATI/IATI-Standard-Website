"""Model definitions for the contact app."""

from wagtail.core.blocks import RichTextBlock, StreamBlock, StructBlock, TextBlock
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from home.models import AbstractContentPage, DefaultPageHeaderImageMixin


class ContactTypeStreamBlock(StreamBlock):
    """Model allowing the CMS to bring together multiple struct block objects."""

    contact_type_editor = StructBlock([
        ('heading', TextBlock()),
        ('description', RichTextBlock(required=False)),
        ('email', TextBlock())
    ], icon='title', classname='title')


class ContactPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """Model to define the overall fields for the contact page."""

    parent_page_types = ['home.HomePage']
    subpage_types = []

    max_count = 1

    contact_type = StreamField(ContactTypeStreamBlock, blank=True, null=True)
    content_panels = AbstractContentPage.content_panels + DefaultPageHeaderImageMixin.content_panels + [
        StreamFieldPanel('contact_type'),
    ]
