# Generated by Django 2.2.9 on 2020-02-21 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_homepage_use_legacy_template'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepage',
            old_name='iati_tools_title_description',
            new_name='iati_tools_description',
        ),
        migrations.RenameField(
            model_name='homepage',
            old_name='iati_tools_title_description_en',
            new_name='iati_tools_description_en',
        ),
        migrations.RenameField(
            model_name='homepage',
            old_name='iati_tools_title_description_es',
            new_name='iati_tools_description_es',
        ),
        migrations.RenameField(
            model_name='homepage',
            old_name='iati_tools_title_description_fr',
            new_name='iati_tools_description_fr',
        ),
        migrations.RenameField(
            model_name='homepage',
            old_name='iati_tools_title_description_pt',
            new_name='iati_tools_description_pt',
        ),
    ]
