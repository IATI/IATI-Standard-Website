from home.models import AbstractContentPage, DefaultPageHeaderImageMixin
from wagtail.core.blocks import RichTextBlock, StreamBlock, StructBlock, TextBlock
from wagtail.core.fields import StreamField


class ContactTypeStreamBlock(StreamBlock):
    """Model allowing the CMS to bring together multiple struct block objects."""
    contact_type_editor = StructBlock([
        ('heading', TextBlock()),
        ('description', RichTextBlock(required=False)),
        ('email', TextBlock())
    ], icon="title", classname="title")


class ContactPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """Model to define the overall fields for the contact page."""
    parent_page_types = ['home.HomePage']
    subpage_types = []
    contact_type = StreamField(ContactTypeStreamBlock, blank=True, null=True)
    translation_fields = AbstractContentPage.translation_fields + ["contact_type"]
