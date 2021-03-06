# Generated by Django 2.2.9 on 2020-04-28 14:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='globalnotice',
            options={'verbose_name_plural': 'Global notice'},
        ),
        migrations.AddField(
            model_name='globalnotice',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='pagenotice',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='pagenotice',
            name='display_location',
            field=models.CharField(choices=[('all', 'All pages in site'), ('selected_page', 'Selected page only'), ('selected_page_and_children', 'Selected page and child pages'), ('children_only', 'Children of selected page')], default='selected_page', max_length=255),
        ),
    ]
