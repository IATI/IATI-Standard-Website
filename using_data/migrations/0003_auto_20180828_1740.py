# Generated by Django 2.0.5 on 2018-08-28 17:40

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('using_data', '0002_toolsindexpage_toolspage'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolsindexpage',
            name='tool_box_editor',
            field=wagtail.core.fields.StreamField((('tool_box_text', wagtail.core.blocks.RichTextBlock(required=False)),), blank=True, null=True),
        ),
        migrations.AddField(
            model_name='toolsindexpage',
            name='tool_box_editor_en',
            field=wagtail.core.fields.StreamField((('tool_box_text', wagtail.core.blocks.RichTextBlock(required=False)),), blank=True, null=True),
        ),
        migrations.AddField(
            model_name='toolsindexpage',
            name='tool_box_editor_es',
            field=wagtail.core.fields.StreamField((('tool_box_text', wagtail.core.blocks.RichTextBlock(required=False)),), blank=True, null=True),
        ),
        migrations.AddField(
            model_name='toolsindexpage',
            name='tool_box_editor_fr',
            field=wagtail.core.fields.StreamField((('tool_box_text', wagtail.core.blocks.RichTextBlock(required=False)),), blank=True, null=True),
        ),
        migrations.AddField(
            model_name='toolsindexpage',
            name='tool_box_editor_pt',
            field=wagtail.core.fields.StreamField((('tool_box_text', wagtail.core.blocks.RichTextBlock(required=False)),), blank=True, null=True),
        ),
    ]