from django.db import models
from django import forms
from wagtail.core.models import Page
from django.utils import translation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.core.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.core.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock


class DocumentChooserULBlock(StreamBlock):
    """A streamblock that holds an arbitrary number of documents"""
    document_single = DocumentChooserBlock(icon="doc-full-inverse", required=False)


class DocumentChooserStream(StreamBlock):
    """A streamblock that holds an arbitrary number of documents"""
    document_box_h2 = CharBlock(icon="title", classname="title", required=False)
    documents_group = DocumentChooserULBlock(icon="doc-full-inverse", required=False)


class DocumentBoxBlock(StructBlock):
    """A block for holding a document box, with a single header and multiple documents"""

    document_box_content = DocumentChooserStream(icon="doc-full-inverse", required=False)


class PullQuoteBlock(StructBlock):
    quote = TextBlock("quote title")

    class Meta:
        icon = "openquote"


class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))


class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = "code"


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock(required=False)


class IATIStreamBlock(StreamBlock):
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

    class Meta:
        abstract = True


class AbstractContentPage(AbstractBasePage):
    """A base for the basic model blocks of all content type pages."""

    content_editor = StreamField(IATIStreamBlock(required=False), null=True, blank=True)

    translation_fields = AbstractBasePage.translation_fields + ["content_editor"]

    class Meta:
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

    class Meta:
        abstract = True


class HomePage(Page):
    translation_fields = []
