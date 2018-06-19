import requests

from django.db import models
from django.conf import settings

from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from home.models import AbstractContentPage, AbstractIndexPage, IATIStreamBlock


class GuidanceAndSupportPage(AbstractContentPage):
    """A base for the Guidance and Support page."""
    parent_page_types = ['home.HomePage']
    subpage_types = ['guidance_and_support.GuidanceGroupPage', 'guidance_and_support.KnowledgebaseIndexPage']

    @property
    def guidance_groups(self):
        """Get all GuidanceGroupPage objects that have been published."""
        guidance_groups = GuidanceGroupPage.objects.child_of(self).live()
        return guidance_groups


class GuidanceGroupPage(AbstractContentPage):
    """A base for Guidance Group pages."""
    subpage_types = ['guidance_and_support.GuidanceGroupPage', 'guidance_and_support.GuidancePage']

    section_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
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


class GuidancePage(AbstractContentPage):
    """A base for a single guidance page."""
    subpage_types = []

    def get_context(self, request):
        """Overwrite context to intercept POST requests to pages on this template and pass them to Zendesk API

        Validate with some sort of captcha."""
        context = super(GuidancePage, self).get_context(request)
        form_success = "none"

        if request.method == 'POST':
            form_success = "failure"
            path = request.path
            captcha = request.POST.get('captcha', 'off') == 'on'
            email = request.POST['email']
            query = request.POST['textarea']
            name = request.POST.get('name', 'Anonymous requester')
            if captcha and email and query:
                request_obj = {
                    "request": {
                        "requester": {"name": name, "email": email},
                        "subject": "Automated request from {}".format(name),
                        "comment": {"body": "A request was sent from {}.\n{}".format(path, query)}
                    }
                }
                response = requests.post("https://iati.zendesk.com/api/v2/requests.json", json=request_obj)
                if response.status_code == 201:
                    form_success = "success"

            context['form_success'] = form_success
        return context


class KnowledgebaseIndexPage(AbstractIndexPage):
    """A base for a Knowledgebase index page."""
    subpage_types = ['guidance_and_support.KnowledgebasePage']


class KnowledgebasePage(AbstractContentPage):
    """A base for a single Knowledgebase page."""
    subpage_types = []
