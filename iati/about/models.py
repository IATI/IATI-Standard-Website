from django.db import models

from wagtail.core.models import Page

class About(Page):
    pass
    # parent_page_types = ['home.HomePage']
    # subpage_types = ['home.AboutSubpage']
