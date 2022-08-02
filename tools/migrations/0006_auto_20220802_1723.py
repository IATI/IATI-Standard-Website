# Generated by Django 3.2.4 on 2022-08-02 17:23

from django.db import migrations
import home.models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0005_auto_20200306_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolpage',
            name='content_editor',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolpage',
            name='content_editor_en',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolpage',
            name='content_editor_es',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolpage',
            name='content_editor_fr',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolpage',
            name='content_editor_pt',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolslistingpage',
            name='content_editor',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolslistingpage',
            name='content_editor_en',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolslistingpage',
            name='content_editor_es',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolslistingpage',
            name='content_editor_fr',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolslistingpage',
            name='content_editor_pt',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolsubpage',
            name='content_editor',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolsubpage',
            name='content_editor_en',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolsubpage',
            name='content_editor_es',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolsubpage',
            name='content_editor_fr',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolsubpage',
            name='content_editor_pt',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False))], icon='image', label='Image figure')), ('pullquote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.TextBlock('quote title'))])), ('aligned_html', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML')), ('document_box', wagtail.core.blocks.StreamBlock([('document_box_heading', wagtail.core.blocks.CharBlock(form_classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))], icon='doc-full-inverse')), ('anchor_point', wagtail.core.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down')), ('fast_youtube_embed', wagtail.core.blocks.URLBlock(icon='fa-video-camera', label='Fast YouTube Embed'))], blank=True, null=True),
        ),
    ]
