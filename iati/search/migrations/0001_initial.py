from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('wagtailsearch', '0003_remove_editors_pick'),
    ]

    operations = [
        migrations.RunSQL(['DROP TABLE IF EXISTS wagtailsearch_editorspick CASCADE;']),
    ]
