# Generated by Django 2.2.9 on 2020-02-27 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('governance', '0002_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='url',
            field=models.URLField(blank=True, help_text='Optional: URL for the member', max_length=255),
        ),
    ]