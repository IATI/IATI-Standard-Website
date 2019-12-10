# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditorsPick',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('sort_order', models.IntegerField(blank=True, null=True, editable=False)),
                ('description', models.TextField(blank=True)),
                ('page', models.ForeignKey(on_delete=models.CASCADE, to='wagtailcore.Page')),
            ],
            options={
                'ordering': ('sort_order',),
                'db_table': 'wagtailsearch_editorspick',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='editorspick',
            name='query',
            field=models.ForeignKey(on_delete=models.CASCADE, to='wagtailsearch.Query', related_name='editors_picks'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='editorspick',
            options={'ordering': ('sort_order',), 'verbose_name': "Editor's Pick"},
        ),
        migrations.AlterField(
            model_name='editorspick',
            name='description',
            field=models.TextField(verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='editorspick',
            name='page',
            field=models.ForeignKey(on_delete=models.CASCADE, verbose_name='Page', to='wagtailcore.Page'),
        ),
    ]
