from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from home.models import AbstractContentPage, AbstractIndexPage, IATIStreamBlock


class GuidanceAndSupportPage(AbstractContentPage):
    parent_page_types = ['home.HomePage']
    subpage_types = ['guidance_and_support.GuidanceIndexPage', 'guidance_and_support.KnowledgebaseIndexPage']

    @property
    def guidance_indexes(self):
        """Get all CaseStudyPage objects that have been published."""
        guidance_indexes = GuidanceIndexPage.objects.child_of(self).live()
        return guidance_indexes


class GuidanceIndexPage(AbstractContentPage):
    subpage_types = ['guidance_and_support.GuidanceIndexPage', 'guidance_and_support.GuidancePage']

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='This is the image that will be displayed for the guidance index page on the main guidance and support page. Ignore if this page is being used as a sub-index page.'
    )

    feed_content = StreamField(IATIStreamBlock(required=False), null=True, blank=True, help_text='A small amount of content to appear on the main page (e.g. bullet points). Ignore if this page is being used as a sub-index page.')

    feed_button_text = models.TextField(max_length=255, null=True, blank=True, help_text='The text to appear on the button of the main guidance and support page. Ignore if this page is being used as a sub-index page.')

    @property
    def guidance_groups(self):
        """Get all objects that are child of self."""
        guidance_groups = Page.objects.child_of(self).specific().live()
        guidance_group_list = [{"page": page, "count": len(page.get_children())} for page in guidance_groups]
        return guidance_group_list

    translation_fields = AbstractContentPage.translation_fields + ["feed_content", "feed_button_text"]

    multilingual_field_panels = [
        ImageChooserPanel('feed_image'),
    ]


class GuidancePage(AbstractContentPage):
    subpage_types = []


class KnowledgebaseIndexPage(AbstractIndexPage):
    subpage_types = ['guidance_and_support.KnowledgebasePage']


class KnowledgebasePage(AbstractContentPage):
    subpage_types = []
