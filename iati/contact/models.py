from django.db import models
from home.models import IATIStreamBlock
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

class ContactPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = []

    subheading = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subheading', classname="full"),
        FieldPanel('description', classname="full")
    ]
