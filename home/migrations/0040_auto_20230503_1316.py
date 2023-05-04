# Generated by Django 3.2.4 on 2023-05-03 13:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0078_referenceindex'),
        ('home', '0039_auto_20230503_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='latestnewsitems',
            name='locale',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale'),
        ),
        migrations.AlterField(
            model_name='latestnewsitems',
            name='translation_key',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='latestnewsitems',
            unique_together={('translation_key', 'locale')},
        ),
    ]
