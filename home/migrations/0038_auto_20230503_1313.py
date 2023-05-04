# Generated by Django 3.2.4 on 2023-05-03 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0078_referenceindex'),
        ('home', '0037_auto_20230503_1312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='latestnewsitems',
            options={},
        ),
        migrations.AddField(
            model_name='latestnewsitems',
            name='locale',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale'),
        ),
        migrations.AddField(
            model_name='latestnewsitems',
            name='translation_key',
            field=models.UUIDField(editable=False, null=True),
        ),
    ]
