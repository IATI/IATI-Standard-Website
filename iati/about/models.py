from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from home.models import IATIStreamBlock


class AbstractAboutPage(Page):
    """
    TODO:
        Decide what to call this and where it should live.
        Create abstract Index page and abstract Content page.

    """
    heading = models.CharField(max_length=255, null=True, blank=True)
    excerpt = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class AboutPage(AbstractAboutPage):
    parent_page_types = ['home.HomePage']
    subpage_types = ['about.AboutSubPage']

    content_editor = StreamField(IATIStreamBlock(required=False), null=True, blank=True)


class AboutSubPage(AbstractAboutPage):
    parent_page_types = ['about.AboutPage']
    subpage_types = []

    content_editor = StreamField(IATIStreamBlock(required=False), null=True, blank=True)


class CaseStudiesIndexPage(AbstractAboutPage):
    parent_page_types = ['about.AboutPage']
    subpage_types = ['about.CaseStudyPage']


class CaseStudyPage(AbstractAboutPage):
    parent_page_types = ['about.CaseStudiesIndexPage']
    subpage_types = []

    content_editor = StreamField(IATIStreamBlock(required=False), null=True, blank=True)

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
