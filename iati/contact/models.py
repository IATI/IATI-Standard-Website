from django.db import models
from home.models import AbstractContentPage
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.blocks import RichTextBlock, StreamBlock, StructBlock, TextBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page


class ContactTypeBlock(StructBlock):
    """Model to define fields relating to a type of query."""
    heading = TextBlock()
    copy = RichTextBlock()
    email = TextBlock()


class ContactTypeStreamBlock(StreamBlock):
    """Model allowing the CMS to bring together multiple ContactTypeBlock objects."""
    contact_type = ContactTypeBlock(icon="title", classname="title")


class ContactPage(AbstractContentPage):
    """Model to define the overall fields for the contact page."""
    parent_page_types = ['home.HomePage']
    subpage_types = []
    contact_type = StreamField(ContactTypeStreamBlock, blank=True, null=True)
    translation_fields = AbstractContentPage.translation_fields + ["contact_type"]
