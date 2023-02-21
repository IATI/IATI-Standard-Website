# Generated by Django 3.2.4 on 2023-01-20 14:56

from django.db import migrations
import home.models
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20220804_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='additional_information',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.blocks.StructBlock([('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock([('document_box_heading', wagtail.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.blocks.URLBlock(icon='code', label='Fast YouTube Embed'))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='additional_information_en',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.blocks.StructBlock([('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock([('document_box_heading', wagtail.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.blocks.URLBlock(icon='code', label='Fast YouTube Embed'))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='additional_information_es',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.blocks.StructBlock([('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock([('document_box_heading', wagtail.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.blocks.URLBlock(icon='code', label='Fast YouTube Embed'))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='additional_information_fr',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.blocks.StructBlock([('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock([('document_box_heading', wagtail.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.blocks.URLBlock(icon='code', label='Fast YouTube Embed'))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='additional_information_pt',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.blocks.StructBlock([('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock([('document_box_heading', wagtail.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.blocks.URLBlock(icon='code', label='Fast YouTube Embed'))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='content_editor',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.blocks.StructBlock([('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock([('document_box_heading', wagtail.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.blocks.URLBlock(icon='code', label='Fast YouTube Embed'))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='content_editor_en',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.blocks.StructBlock([('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock([('document_box_heading', wagtail.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.blocks.URLBlock(icon='code', label='Fast YouTube Embed'))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='content_editor_es',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.blocks.StructBlock([('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock([('document_box_heading', wagtail.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.blocks.URLBlock(icon='code', label='Fast YouTube Embed'))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='content_editor_fr',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.blocks.StructBlock([('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock([('document_box_heading', wagtail.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.blocks.URLBlock(icon='code', label='Fast YouTube Embed'))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='content_editor_pt',
            field=wagtail.fields.StreamField([('h2', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.blocks.StructBlock([('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock([('document_box_heading', wagtail.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.blocks.URLBlock(icon='code', label='Fast YouTube Embed'))], blank=True, null=True, use_json_field=True),
        ),
    ]
