# Generated by Django 2.2.9 on 2020-02-27 10:20

from django.db import migrations, models
import django.db.models.deletion
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('taxonomies', '0001_initial'),
        ('governance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('name_en', models.CharField(max_length=255, null=True, unique=True)),
                ('name_fr', models.CharField(max_length=255, null=True, unique=True)),
                ('name_es', models.CharField(max_length=255, null=True, unique=True)),
                ('name_pt', models.CharField(max_length=255, null=True, unique=True)),
                ('date_joined', models.DateField(help_text='Year that the member joined')),
                ('constituency', models.ForeignKey(help_text='The constituency of the member', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='taxonomies.Constituency')),
                ('image', models.ForeignKey(blank=True, help_text='Optional: image for the member', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]
