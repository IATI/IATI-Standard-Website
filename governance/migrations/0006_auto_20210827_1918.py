# Generated by Django 3.2.4 on 2021-08-27 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('governance', '0005_member_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chairitems',
            name='bio_en',
        ),
        migrations.RemoveField(
            model_name='chairitems',
            name='bio_es',
        ),
        migrations.RemoveField(
            model_name='chairitems',
            name='bio_fr',
        ),
        migrations.RemoveField(
            model_name='chairitems',
            name='bio_pt',
        ),
        migrations.RemoveField(
            model_name='chairitems',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='chairitems',
            name='name_es',
        ),
        migrations.RemoveField(
            model_name='chairitems',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='chairitems',
            name='name_pt',
        ),
        migrations.RemoveField(
            model_name='member',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='member',
            name='name_es',
        ),
        migrations.RemoveField(
            model_name='member',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='member',
            name='name_pt',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='content_editor_en',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='content_editor_es',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='content_editor_fr',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='content_editor_pt',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='excerpt_en',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='excerpt_es',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='excerpt_fr',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='excerpt_pt',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='heading_en',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='heading_es',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='heading_fr',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='heading_pt',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='members_title_en',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='members_title_es',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='members_title_fr',
        ),
        migrations.RemoveField(
            model_name='membersassemblypage',
            name='members_title_pt',
        ),
        migrations.RemoveField(
            model_name='vicechairitems',
            name='bio_en',
        ),
        migrations.RemoveField(
            model_name='vicechairitems',
            name='bio_es',
        ),
        migrations.RemoveField(
            model_name='vicechairitems',
            name='bio_fr',
        ),
        migrations.RemoveField(
            model_name='vicechairitems',
            name='bio_pt',
        ),
        migrations.RemoveField(
            model_name='vicechairitems',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='vicechairitems',
            name='name_es',
        ),
        migrations.RemoveField(
            model_name='vicechairitems',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='vicechairitems',
            name='name_pt',
        ),
    ]
