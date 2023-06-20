# Generated by Django 2.0.5 on 2018-06-26 12:21

from django.db import migrations, models
import django.db.models.deletion
import home.models
import wagtail.blocks
import wagtail.fields
import wagtail.documents.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='IATIStandardPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('heading', models.CharField(blank=True, max_length=255, null=True)),
                ('heading_en', models.CharField(blank=True, max_length=255, null=True)),
                ('heading_fr', models.CharField(blank=True, max_length=255, null=True)),
                ('heading_es', models.CharField(blank=True, max_length=255, null=True)),
                ('heading_pt', models.CharField(blank=True, max_length=255, null=True)),
                ('excerpt', models.TextField(blank=True, null=True)),
                ('excerpt_en', models.TextField(blank=True, null=True)),
                ('excerpt_fr', models.TextField(blank=True, null=True)),
                ('excerpt_es', models.TextField(blank=True, null=True)),
                ('excerpt_pt', models.TextField(blank=True, null=True)),
                ('content_editor', wagtail.fields.StreamField((('h2', wagtail.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))), icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock((('quote', wagtail.blocks.TextBlock('quote title')),))), ('aligned_html', wagtail.blocks.StructBlock((('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())), icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock((('document_box_heading', wagtail.blocks.CharBlock(classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))), icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down'))), blank=True, null=True)),
                ('content_editor_en', wagtail.fields.StreamField((('h2', wagtail.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))), icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock((('quote', wagtail.blocks.TextBlock('quote title')),))), ('aligned_html', wagtail.blocks.StructBlock((('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())), icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock((('document_box_heading', wagtail.blocks.CharBlock(classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))), icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down'))), blank=True, null=True)),
                ('content_editor_fr', wagtail.fields.StreamField((('h2', wagtail.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))), icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock((('quote', wagtail.blocks.TextBlock('quote title')),))), ('aligned_html', wagtail.blocks.StructBlock((('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())), icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock((('document_box_heading', wagtail.blocks.CharBlock(classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))), icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down'))), blank=True, null=True)),
                ('content_editor_es', wagtail.fields.StreamField((('h2', wagtail.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))), icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock((('quote', wagtail.blocks.TextBlock('quote title')),))), ('aligned_html', wagtail.blocks.StructBlock((('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())), icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock((('document_box_heading', wagtail.blocks.CharBlock(classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))), icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down'))), blank=True, null=True)),
                ('content_editor_pt', wagtail.fields.StreamField((('h2', wagtail.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('image_figure', wagtail.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment', home.models.ImageAlignmentChoiceBlock()), ('caption', wagtail.blocks.RichTextBlock(required=False))), icon='image', label='Image figure')), ('pullquote', wagtail.blocks.StructBlock((('quote', wagtail.blocks.TextBlock('quote title')),))), ('aligned_html', wagtail.blocks.StructBlock((('html', wagtail.blocks.RawHTMLBlock()), ('alignment', home.models.HTMLAlignmentChoiceBlock())), icon='code', label='Raw HTML')), ('document_box', wagtail.blocks.StreamBlock((('document_box_heading', wagtail.blocks.CharBlock(classname='title', help_text='Only one heading per box.', icon='title', required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', required=False))), icon='doc-full-inverse')), ('anchor_point', wagtail.blocks.CharBlock(help_text='Custom anchor points are expected to precede other content.', icon='order-down'))), blank=True, null=True)),
                ('header_image', models.ForeignKey(blank=True, help_text='This is the image that will appear in the header banner at the top of the page. If no image is added a placeholder image will be used.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
