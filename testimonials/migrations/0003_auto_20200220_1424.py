# Generated by Django 2.2.9 on 2020-02-20 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0002_auto_20200214_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonial',
            name='quotee',
            field=models.TextField(help_text='The source of the quote'),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='quotee_en',
            field=models.TextField(help_text='The source of the quote', null=True),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='quotee_es',
            field=models.TextField(help_text='The source of the quote', null=True),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='quotee_fr',
            field=models.TextField(help_text='The source of the quote', null=True),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='quotee_pt',
            field=models.TextField(help_text='The source of the quote', null=True),
        ),
    ]
