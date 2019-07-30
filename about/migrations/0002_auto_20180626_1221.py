# Generated by Django 2.0.5 on 2018-06-26 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('about', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutpage',
            name='header_image',
            field=models.ForeignKey(blank=True, help_text='This is the image that will appear in the header banner at the top of the page. If no image is added a placeholder image will be used.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='casestudyindexpage',
            name='header_image',
            field=models.ForeignKey(blank=True, help_text='This is the image that will appear in the header banner at the top of the page. If no image is added a placeholder image will be used.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AlterField(
            model_name='casestudypage',
            name='feed_image',
            field=models.ForeignKey(blank=True, help_text='This is the image that will be displayed for the case study in the page header and on the Case Studies list page.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]