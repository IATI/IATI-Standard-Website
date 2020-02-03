# pylint: disable=too-many-locals, duplicate-code
"""Management command that loads locale .po files into database."""

from __future__ import unicode_literals
import json
from os.path import join, isdir
from django.conf import settings

from django.core.management.base import BaseCommand as LoadCommand, CommandError
from django.apps import apps
from babel.messages.pofile import read_po


def setattr_by_json_path(json_object, path, value):
    first_id = path.find("#")
    second_id = path.find("#", first_id + 1)
    first_key = path.find("/")
    second_key = path.find("/", first_key + 1)
    indices = [x for x in [first_id, second_id, first_key, second_key] if x > 0]
    indices.sort()
    indices.append(len(path) + 1)

    if path[0] == "#" and isinstance(json_object, list):
        child_id = path[1:indices[0]]
        path_remainder = path[indices[0]:]
        for sub_object in json_object:
            try:
                if sub_object["id"] == child_id:
                    setattr_by_json_path(sub_object, path_remainder, value)
            except KeyError:
                pass
    elif path[0] == "/" and isinstance(json_object, dict):
        child_key = path[1:indices[0]]
        path_remainder = path[indices[0]:]
        try:
            sub_object = json_object[child_key]
            if isinstance(sub_object, str):
                json_object[child_key] = value
            else:
                setattr_by_json_path(sub_object, path_remainder, value)
        except KeyError:
            pass
    return json_object


class Command(LoadCommand):
    """Management command that loads locale .po files into database."""

    def handle(self, *args, **options):
        """Handle the load_trans command."""
        po_filename = "nav.po"
        locale_path = settings.MODELTRANSLATION_LOCALE_PATH
        if not isdir(locale_path):
            raise CommandError("Locale directory does not exists.")
        for lang in [l[0] for l in list(settings.LANGUAGES)]:
            if lang != "en":
                lang_path = join(locale_path, lang)
                if not isdir(lang_path):
                    raise CommandError("Language directory does not exists.")
                po_file = open(join(lang_path, "LC_MESSAGES", po_filename), "r", encoding="utf-8")
                catalog = read_po(po_file)
                po_file.close()
                for message in catalog:
                    if message.string not in [None, "None", ""] and message.auto_comments:
                        for field_id in message.auto_comments:
                            [app, class_name, primary_key, field, json_path] = field_id.split('.')
                            model = apps.get_model(app, class_name)
                            try:
                                obj = model.objects.get(pk=primary_key)
                            except model.DoesNotExist:
                                continue
                            if json_path == "":
                                setattr(obj, field, message.string)
                                obj.save()
                            else:
                                msg_data = getattr(obj, field).stream_data
                                tr_json_path = "%s_%s" % (json_path[:-3], lang)
                                msg_data = setattr_by_json_path(msg_data, tr_json_path, message.string)
                                setattr(obj, field, json.dumps(msg_data))
                                obj.save()
