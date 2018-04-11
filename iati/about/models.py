from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from home.models import IATIStreamBlock


class AboutPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['about.AboutSubPage']

    heading = models.CharField(max_length=255, null=True, blank=True)
    excerpt = models.TextField(null=True, blank=True)
    content_editor = StreamField(IATIStreamBlock(required=False), null=True, blank=True)


class AboutSubPage(Page):
    parent_page_types = ['about.AboutPage']
    subpage_types = []

    heading = models.CharField(max_length=255, null=True, blank=True)
    excerpt = models.TextField(null=True, blank=True)
    content_editor = StreamField(IATIStreamBlock(required=False), null=True, blank=True)

# class CaseStudyPage(Page):
#     parent_page_types = ['about.AboutSubPage']
#     subpage_types = []

#fffunction notes:

# Model would be something like:
#
## title
## intro (text area)
# content_editor
# The members assembly block in the sidebar is an optional item, the model for which should be something like:
#
# block_title
# block_content
# block_button_text
# block_button_url
# This block appears on several templates
