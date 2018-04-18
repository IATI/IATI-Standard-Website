from django.db import models
from home.models import AbstractContentPage
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

class ContactPage(AbstractContentPage):
    parent_page_types = ['home.HomePage']
    subpage_types = []
