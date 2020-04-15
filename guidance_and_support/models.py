"""Model definitions for the guidance_and_support app."""

from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from home.models import AbstractContentPage, AbstractIndexPage, DefaultPageHeaderImageMixin, IATIStreamBlock
from .mixins import ContactFormMixin


class GuidanceAndSupportPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """A base for the Guidance and Support page."""

    parent_page_types = ['home.HomePage']
    subpage_types = [
        'guidance_and_support.GuidanceGroupPage',
        'guidance_and_support.SupportPage',
        # 'guidance_and_support.KnowledgebaseIndexPage',
    ]

    max_count = 1

    @property
    def guidance_groups(self):
        """Get all GuidanceGroupPage objects that have been published."""
        guidance_groups = GuidanceGroupPage.objects.child_of(self).live()
        return guidance_groups


class GuidanceGroupPage(AbstractContentPage):
    """A base for Guidance Group pages."""

    parent_page_types = [
        'guidance_and_support.GuidanceAndSupportPage',
        'guidance_and_support.GuidanceGroupPage',
    ]
    subpage_types = [
        'guidance_and_support.GuidanceGroupPage',
        'guidance_and_support.GuidancePage',
    ]

    section_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+',
        help_text='This is the image that will be displayed for this page on the main guidance and support page. Ignore if this page is being used as a sub-index page.'
    )

    section_summary = StreamField(IATIStreamBlock(required=False), null=True, blank=True, help_text='A small amount of content to appear on the main page (e.g. bullet points). Ignore if this page is being used as a sub-index page.')

    button_link_text = models.TextField(max_length=255, null=True, blank=True, help_text='The text to appear on the button of the main guidance and support page. Ignore if this page is being used as a sub-index page.')

    content_editor = StreamField(IATIStreamBlock(required=False), null=True, blank=True, help_text='The content to appear on the page itself, as opposed to "section summary" which appears on the parent page.')

    @property
    def guidance_groups(self):
        """Get all objects that are children of the instantiated GuidanceGroupPage.

        Note:
            These can be other guidance group pages or single guidance pages.

        """
        guidance_groups = Page.objects.child_of(self).specific().live()
        guidance_group_list = [{"page": page, "count": len(page.get_children())} for page in guidance_groups]
        return guidance_group_list

    translation_fields = AbstractContentPage.translation_fields + ["section_summary", "button_link_text"]

    multilingual_field_panels = [
        ImageChooserPanel('section_image'),
    ]


class GuidancePage(ContactFormMixin, AbstractContentPage):
    """A base for a single guidance page."""

    parent_page_types = ['guidance_and_support.GuidanceGroupPage']
    subpage_types = []


# class KnowledgebaseIndexPage(AbstractIndexPage):
#     """A base for a Knowledgebase index page."""

#     subpage_types = ['guidance_and_support.KnowledgebasePage']


# class KnowledgebasePage(AbstractContentPage):
#     """A base for a single Knowledgebase page."""

#     subpage_types = []


class CommunityPage(DefaultPageHeaderImageMixin, AbstractIndexPage):
    """A base for the Community page."""

    parent_page_types = ['home.HomePage']
    subpage_types = []

    max_count = 1

    text_box = models.TextField(max_length=255, null=True, blank=True, help_text='A small ammount of text describing the community page.')

    button_link_text = models.CharField(max_length=255, null=True, blank=True, help_text='The text to appear on the button of the community page.')

    button_url = models.URLField(null=True, blank=True, help_text='The url for the community page being linked')

    translation_fields = AbstractIndexPage.translation_fields + ["text_box", "button_link_text"]

    content_panels = AbstractIndexPage.content_panels + [
        FieldPanel('heading'),
        FieldPanel('button_link_text'),
        FieldPanel('button_url'),
        FieldPanel('text_box')
    ]


class SupportPage(DefaultPageHeaderImageMixin, ContactFormMixin, AbstractContentPage):
    """Model to define the overall fields for the support page."""

    parent_page_types = ['guidance_and_support.GuidanceAndSupportPage']
    subpage_types = []

    max_count = 1

    alternative_content = RichTextField(
        features=['h3', 'link', 'ul'],
        help_text='Content to describe alternative ways of receiving support',
    )

    translation_fields = AbstractContentPage.translation_fields + [
        'alternative_content',
    ]
