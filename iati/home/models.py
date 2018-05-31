"""Model definitions for the home app."""

from django.db import models
from django import forms
from wagtail.core.models import Page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.core.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.core.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.blocks import DocumentChooserBlock


class DocumentBoxBlock(StreamBlock):
    """A block for holding a document box, with a single header and multiple documents"""

    document_box_heading = CharBlock(icon="title", classname="title", required=False, help_text="Only one heading per box.")
    document = DocumentChooserBlock(icon="doc-full-inverse", required=False)


class PullQuoteBlock(StructBlock):
    """A block for creating a pull quote"""
    quote = TextBlock("quote title")

    class Meta(object):
        """Meta data for the class"""
        icon = "openquote"


class ImageAlignmentChoiceBlock(FieldBlock):
    """A block which contains the choices and class names for image alignment"""
    field = forms.ChoiceField(choices=(
        ('media-figure', "Full width"),
        ('media-figure--center', "Small centered"),
        ('media-figure--alignleft', "Align left"),
        ('media-figure--alignright', "Align right")
    ))


class HTMLAlignmentChoiceBlock(FieldBlock):
    """A block which contains the choices and class names for HTML alignment"""
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))


class AlignedHTMLBlock(StructBlock):
    """A block which allows for raw HTML entry and alignment"""
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta(object):
        """Meta data for the class"""
        icon = "code"


class ImageBlock(StructBlock):
    """A block which allows for image entry and alignment"""
    image = ImageChooserBlock()
    alignment = ImageAlignmentChoiceBlock()
    caption = RichTextBlock(required=False)


class IATIStreamBlock(StreamBlock):
    """The main stream block used as the content editor sitewide"""
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    image_figure = ImageBlock(label="Image figure", icon="image")
    pullquote = PullQuoteBlock()
    aligned_html = AlignedHTMLBlock(icon="code", label='Raw HTML')
    document_box = DocumentBoxBlock(icon="doc-full-inverse")


class AbstractBasePage(Page):
    """A base for all page types."""
    heading = models.CharField(max_length=255, null=True, blank=True)
    excerpt = models.TextField(null=True, blank=True)

    translation_fields = [
        "heading",
        "excerpt"
    ]

    class Meta(object):
        """Meta data for the class"""
        abstract = True


class AbstractContentPage(AbstractBasePage):
    """A base for the basic model blocks of all content type pages."""

    content_editor = StreamField(IATIStreamBlock(required=False), null=True, blank=True)

    translation_fields = AbstractBasePage.translation_fields + ["content_editor"]

    class Meta(object):
        """Meta data for the class"""
        abstract = True


class AbstractIndexPage(AbstractBasePage):
    """"A base for the basic model block of all index type pages."""

    def filter_children(self, queryset, filter_dict):
        """Take a dict of filters and apply filters to child queryset."""
        return queryset.filter(**filter_dict)

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
        """Meta data for the class"""
        abstract = True


class HomePage(AbstractBasePage):  # pylint: disable=too-many-ancestors
    """Proof-of-concept model definition for the homepage."""
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='This is the image that will appear in the header banner at the top of the Home Page. If no image is added a placeholder image will be used.'
    )
    multilingual_field_panels = [
        ImageChooserPanel('header_image')
    ]
