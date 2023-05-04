# Generated by Django 3.2.4 on 2023-05-02 12:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0078_referenceindex'),
        ('home', '0030_auto_20230502_1220'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='iatiinactionfeatureditems',
            options={},
        ),
        migrations.AlterField(
            model_name='iatiinactionfeatureditems',
            name='locale',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale'),
        ),
        migrations.AlterField(
            model_name='iatiinactionfeatureditems',
            name='translation_key',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='iatiinactionfeatureditems',
            unique_together={('translation_key', 'locale')},
        ),
    ]
