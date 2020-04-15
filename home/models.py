"""Model definitions for the home app."""
import re

from django.conf import settings
from django.db import models
from django.apps import apps
from django import forms
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import slugify
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.core.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock, PageChooserBlock
from wagtail.core.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.search.index import FilterField, SearchField
from home.fields import HomeFieldsMixin
from home.inlines import GettingStartedItems  # noqa


class DocumentBoxBlock(StreamBlock):
    """A block for holding a document box, with a single header and multiple documents."""

    document_box_heading = CharBlock(icon="title", classname="title", required=False, help_text="Only one heading per box.")
    document = DocumentChooserBlock(icon="doc-full-inverse", required=False)


class PullQuoteBlock(StructBlock):
    """A block for creating a pull quote."""

    quote = TextBlock("quote title")

    class Meta(object):
        """Meta data for the class."""

        icon = "openquote"


class ImageAlignmentChoiceBlock(FieldBlock):
    """A block which contains the choices and class names for image alignment."""

    field = forms.ChoiceField(choices=(
        ('media-figure', "Full width"),
        ('media-figure--center', "Small centered"),
        ('media-figure--alignleft', "Align left"),
        ('media-figure--alignright', "Align right")
    ))


class HTMLAlignmentChoiceBlock(FieldBlock):
    """A block which contains the choices and class names for HTML alignment."""

    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))


class AlignedHTMLBlock(StructBlock):
    """A block which allows for raw HTML entry and alignment."""

    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta(object):
        """Meta data for the class."""

        icon = "code"


class ImageBlock(StructBlock):
    """A block which allows for image entry and alignment."""

    image = ImageChooserBlock()
    alignment = ImageAlignmentChoiceBlock()
    caption = RichTextBlock(required=False)


class HighlightBlock(StructBlock):
    """A block for a highlight module."""

    class Meta:
        """Meta data for the class."""

        icon = 'pick'

    title = CharBlock(icon="title")
    description = CharBlock(icon="pilcrow")
    page = PageChooserBlock(icon="link")
    link_label = CharBlock(icon="link")


def highlight_streamfield():
    """Return a streamfield which only allows one highlight block."""
    return StreamField(
        StreamBlock(
            [
                ('highlight', HighlightBlock()),
            ],
            max_num=1,
            required=False,
        ),
        blank=True,
    )


class IATIStreamBlock(StreamBlock):
    """The main stream block used as the content editor sitewide."""

    h2 = CharBlock(icon="title", classname="title")  # pylint: disable=invalid-name
    h3 = CharBlock(icon="title", classname="title")  # pylint: disable=invalid-name
    h4 = CharBlock(icon="title", classname="title")  # pylint: disable=invalid-name
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    image_figure = ImageBlock(label="Image figure", icon="image")
    pullquote = PullQuoteBlock()
    aligned_html = AlignedHTMLBlock(icon="code", label='Raw HTML')
    document_box = DocumentBoxBlock(icon="doc-full-inverse")
    anchor_point = CharBlock(icon="order-down", help_text="Custom anchor points are expected to precede other content.")

    def get_searchable_content(self, value):
        """Overidden method to fix None type errors on indexing."""
        content = []

        if value:
            for child in value:
                content.extend(child.block.get_searchable_content(child.value))

        return content


class AbstractBasePage(Page):
    """A base for all page types."""

    heading = models.CharField(max_length=255, null=True, blank=True)
    excerpt = models.TextField(null=True, blank=True)
    social_media_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+',
        help_text='This image will be used as the image for social media sharing cards.'
    )

    translation_fields = [
        "heading",
        "excerpt"
    ]
    search_fields = Page.search_fields + [
        FilterField('live'),
        SearchField('heading'),
        SearchField('excerpt'),
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('social_media_image'),
    ]

    class Meta(object):
        """Meta data for the class."""

        abstract = True

    def get_context(self, request, *args, **kwargs):
        """Override get_context method to check for active language length."""
        context = super(AbstractBasePage, self).get_context(request, *args, **kwargs)
        context['has_multilanguage_support'] = len(settings.ACTIVE_LANGUAGES)
        context['social_twitter_handle'] = settings.TWITTER_HANDLE
        context['social_youtube_url'] = settings.YOUTUBE_CHANNEL_URL
        return context

    def clean(self):
        """Override clean to remove trailing dashes from slugs with whitespaces."""
        for lang in tuple(x[0] for x in settings.LANGUAGES):
            slug_field = 'slug_{}'.format(lang)
            slug = getattr(self, slug_field)
            if slug:
                slug_stripped = re.sub(r'[^\w\s-]', '', slug).strip("-")
                slug_valid = slugify(slug_stripped)
                setattr(self, slug_field, slug_valid)
        super(AbstractBasePage, self).clean()

    @property
    def social_share_image_url(self):
        """Return a default social media image for any page."""
        if self.social_media_image:
            return self.social_media_image.get_rendition('min-300x300|jpegquality-60').url
        if hasattr(self, 'feed_image'):
            if self.feed_image:
                return self.feed_image.get_rendition('min-300x300|jpegquality-60').url
        return static(settings.DEFAULT_SHARE_IMAGE_URL)

    @property
    def search_display_name(self):
        """Return the verbose name for search display."""
        return self._meta.verbose_name.replace(' page', '')

    @property
    def search_display_date(self):
        """Return a date for search display."""
        return ''


class AbstractContentPage(AbstractBasePage):
    """A base for the basic model blocks of all content type pages."""

    content_editor = StreamField(IATIStreamBlock(required=False), null=True, blank=True)

    translation_fields = AbstractBasePage.translation_fields + ["content_editor"]
    search_fields = AbstractBasePage.search_fields + [SearchField('content_editor')]

    class Meta(object):
        """Meta data for the class."""

        abstract = True


class AbstractIndexPage(AbstractBasePage):
    """A base for the basic model block of all index type pages."""

    def filter_children(self, queryset, filter_dict):
        """Take a dict of filters and apply filters to child queryset."""
        return queryset.filter(**filter_dict)

    def _get_paginator_range(self, pages):
        """Return a 10 elements long list containing a range of page numbers (int)."""
        range_start = pages.number - 5 if pages.number > 5 else 1
        if pages.number < (pages.paginator.num_pages - 4):
            range_end = pages.number + 4
        else:
            range_end = pages.paginator.num_pages
        return [i for i in range(range_start, range_end + 1)]

    def paginate(self, request, queryset, max_results):
        """Paginate querysets of AbstractIndexPage children.

        TODO:
            Consider how we want to handle unexpected user input.

        """
        page = request.GET.get('page')
        paginator = Paginator(queryset, max_results)
        try:
            return paginator.page(page)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return paginator.page(paginator.num_pages)

    class Meta(object):
        """Meta data for the class."""

        abstract = True


class DefaultPageHeaderImageMixin(Page):
    """A mixin to add a Multilingual tab with the ability to edit the header image for default pages.

    As only default pages require an editable header image this mixin allows selective inclusion alongside other inherited abstract page models.

    """

    header_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+',
        help_text='This is the image that will appear in the header banner at the top of the page. If no image is added a placeholder image will be used.'
    )
    multilingual_field_panels = [
        ImageChooserPanel('header_image')
    ]

    class Meta(object):
        """Meta data for the class."""

        abstract = True


class HomePage(DefaultPageHeaderImageMixin, HomeFieldsMixin, AbstractBasePage):  # pylint: disable=too-many-ancestors
    """Proof-of-concept model definition for the homepage."""

    max_count = 1

    activities = models.PositiveIntegerField(default=1000000)
    organisations = models.PositiveIntegerField(default=700)

    local_translation_fields = [
        'header_video',
        'activities_description',
        'organisations_description',
        'getting_started_title',
        'about_iati_title',
        'about_iati_description',
        'about_iati_video',
        'about_iati_link_label',
        'iati_in_action_title',
        'iati_in_action_description',
        'iati_tools_title',
        'iati_tools_description',
        'latest_news_title',
        'latest_news_link_label',
        'latest_news_tweets_title',
    ]
    optional_local_translation_fields = [
        'header_video',
        'about_iati_video',
        'iati_in_action_description',
        'iati_tools_description',
    ]
    translation_fields = AbstractBasePage.translation_fields + local_translation_fields
    required_languages = {'en': list(set(local_translation_fields) - set(optional_local_translation_fields))}

    def get_context(self, request, *args, **kwargs):
        """Overwrite the default get_context page to serve descendant case study pages."""
        case_study_page = apps.get_model(app_label='about', model_name='CaseStudyPage')
        case_studies = case_study_page.objects.live().descendant_of(self).specific()
        context = super(HomePage, self).get_context(request)
        context['case_studies'] = case_studies
        return context

    def get_template(self, request, *args, **kwargs):
        """Return template based on flag."""
        template = 'home/home_page.html'
        if self.use_legacy_template:
            template = 'home/home_page_legacy.html'
        return template

    multilingual_field_panels = DefaultPageHeaderImageMixin.multilingual_field_panels + [
        FieldPanel('use_legacy_template'),
        InlinePanel(
            'testimonial_items',
            heading='Testimonial items',
            label='Testimonial item',
            min_num=1,
        ),
        FieldPanel('activities'),
        FieldPanel('organisations'),
        InlinePanel(
            'getting_started_items',
            heading='Getting started items',
            label='Getting started item',
            min_num=3,
            max_num=3,
        ),
        PageChooserPanel('about_iati_page'),
        InlinePanel(
            'iati_in_action_featured_item',
            heading='IATI in action featured item',
            label='IATI in action featured item',
            min_num=1,
            max_num=1,
        ),
        InlinePanel(
            'iati_in_action_items',
            heading='IATI in action items',
            label='IATI in action item',
            min_num=2,
            max_num=2,
        ),
        InlinePanel(
            'iati_tools_items',
            heading='IATI tools items',
            label='IATI tools item',
            min_num=2,
            max_num=2,
        ),
        InlinePanel(
            'latest_news_items',
            heading='Latest news items',
            label='Latest news item',
            max_num=3,
        ),
    ]


class StandardPage(AbstractContentPage):
    """A standard content page for generic use, i.e. a Privacy page."""

    parent_page_types = [
        'home.HomePage',
        'home.StandardPage',
    ]
    subpage_types = ['home.StandardPage']

    FIXED_PAGE_TYPES = (
        ("privacy", "Privacy"),
        ("terms", "Terms and conditions"),
        ("trans", "Translation FAQs"),
    )
    fixed_page_type = models.CharField(max_length=7, choices=FIXED_PAGE_TYPES, null=True, blank=True)

    multilingual_field_panels = [
        FieldPanel('fixed_page_type'),
    ]
