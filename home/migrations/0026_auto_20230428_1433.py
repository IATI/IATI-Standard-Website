# Generated by Django 3.2.4 on 2023-04-28 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0078_referenceindex'),
        ('home', '0025_auto_20230425_1139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gettingstarteditems',
            options={},
        ),
        migrations.AddField(
            model_name='gettingstarteditems',
            name='locale',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale'),
        ),
        migrations.AddField(
            model_name='gettingstarteditems',
            name='translation_key',
            field=models.UUIDField(editable=False, null=True),
        ),
    ]
