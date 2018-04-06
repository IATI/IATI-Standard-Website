from django.db import models
from django import forms
from wagtail.core.models import Page
from django.utils import translation

from wagtail.core.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

class TranslatedField:
    def __init__(self,en_field,fr_field,es_field):
        self.en_field = en_field
        self.fr_field = fr_field
        self.es_field = es_field
        
    def __get__(self,instance,owner):
        if translation.get_language() == 'fr':
            return getattr(instance,self.fr_field)
        elif translation.get_language() == 'es':
            return getattr(instance,self.es_field)
        #The default
        else:
            return getattr(instance,self.en_field)
        
class PullQuoteBlock(StructBlock):
    quote = TextBlock("quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"
        
class EndNoteBlock(StructBlock):
    number = CharBlock()
    citation = RichTextBlock(required=False)
        
class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))

class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = "code"
        
class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'), ('mid', 'Mid width'), ('full', 'Full width'),
    ))

class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock(required=False)
    alignment = ImageFormatChoiceBlock()

class IATIStreamBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    endnote = EndNoteBlock()
    aligned_image = ImageBlock(label="Aligned image", icon="image")
    pullquote = PullQuoteBlock()
    aligned_html = AlignedHTMLBlock(icon="code", label='Raw HTML')
    document = DocumentChooserBlock(icon="doc-full-inverse")

class HomePage(Page):
    pass
