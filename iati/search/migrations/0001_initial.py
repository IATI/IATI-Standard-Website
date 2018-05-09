from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('wagtailsearch', '0003_remove_editors_pick'),
    ]

    operations = [
        # migrations.RunSQL('ALTER TABLE wagtailsearch_editorspick DROP CONSTRAINT wagtailsearch_editor_page_id_28cbc274_fk_wagtailco;'),
        migrations.RunSQL('DROP TABLE IF EXISTS wagtailsearch_editorspick CASCADE;'),
    ]
