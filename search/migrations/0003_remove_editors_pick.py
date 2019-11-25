# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('search', '0002_recreate_wagtail_search'),
    ]

    operations = [
        # EditorsPicks have been moved to the "wagtailsearchpromotions" module.

        # Remove EditorsPick from wagtailsearch but don't drop the underlying table
        # so wagtailsearchpromotions can pick it up in its initial migration.

        # If wagtailsearchpromotions isn't installed, this table will remain
        # in the database unmanaged until it is. This could potentially happen
        # at any point in the future so it's important to keep this behaviour
        # even if we decide to squash these migrations.
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='editorspick',
                    name='page',
                ),
                migrations.RemoveField(
                    model_name='editorspick',
                    name='query',
                ),
                migrations.DeleteModel(
                    name='editorspick',
                ),
            ],
            database_operations=[],
        )
    ]
