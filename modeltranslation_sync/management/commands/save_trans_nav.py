# pylint: disable=too-many-locals, too-many-branches, duplicate-code, R0101
"""Management command that saves locale .po files from database."""

from __future__ import unicode_literals
import json
from os import mkdir
from os.path import join, isdir, exists

from wagtail.core.blocks.stream_block import StreamValue

from django.core.management.base import BaseCommand
from django.conf import settings
from babel.messages.catalog import Catalog
from babel.messages.pofile import read_po, write_po
from navigation.models import PrimaryMenuLinks, UtilityMenuLinks, UsefulLinksMenu


def generate_json_paths(json_object, path, path_object):
    if isinstance(json_object, list):
        for sub_object in json_object:
            try:
                new_path = path + "#{}".format(sub_object["id"])
                path_object = generate_json_paths(sub_object, new_path, path_object)
            except KeyError:
                pass
    elif isinstance(json_object, dict):
        for sub_key in json_object.keys():
            new_path = path + "/{}".format(sub_key)
            sub_object = json_object[sub_key]
            path_object = generate_json_paths(sub_object, new_path, path_object)
    elif isinstance(json_object, str):
        path_object[path] = str(json_object)
    return path_object


def fetch_json_by_path(json_object, path):
    first_id = path.find("#")
    second_id = path.find("#", first_id + 1)
    first_key = path.find("/")
    second_key = path.find("/", first_key + 1)
    indices = [x for x in [first_id, second_id, first_key, second_key] if x > 0]
    indices.sort()
    indices.append(len(path) + 1)
    if isinstance(json_object, str):
        return str(json_object)
    elif path[0] == "#" and isinstance(json_object, list):
        child_id = path[1:indices[0]]
        path_remainder = path[indices[0]:]
        for sub_object in json_object:
            try:
                if sub_object["id"] == child_id:
                    return fetch_json_by_path(sub_object, path_remainder)
            except KeyError:
                pass
    elif path[0] == "/" and isinstance(json_object, dict):
        child_key = path[1:indices[0]]
        path_remainder = path[indices[0]:]
        try:
            sub_object = json_object[child_key]
            return fetch_json_by_path(sub_object, path_remainder)
        except KeyError:
            pass
    return None


class Command(BaseCommand):
    """Management command that saves locale .po files from database."""

    def handle(self, *args, **options):
        """Handle the save_trans command."""
        filename_po = "nav.po"

        locale_path = settings.MODELTRANSLATION_LOCALE_PATH
        if not isdir(locale_path):
            mkdir(locale_path)

        for lang in [l[0] for l in list(settings.LANGUAGES)]:

            word_count = 0

            lang_path = join(locale_path, lang)
            if not isdir(lang_path):
                mkdir(lang_path)
                mkdir(join(lang_path, "LC_MESSAGES"))

            po_filepath = join(lang_path, "LC_MESSAGES", filename_po)
            existing_ids = []
            existing_trans = {}
            if exists(po_filepath):
                print(po_filepath)
                po_file = open(po_filepath, "r", encoding="utf-8")
                catalog = read_po(po_file)
                po_file.close()
                for message in catalog:
                    existing_ids.append(message.id)
                    for auto_comment in message.auto_comments:
                        existing_trans[auto_comment] = message.id
            else:
                catalog = Catalog(locale=lang)

            to_translate = []

            for model in [PrimaryMenuLinks, UtilityMenuLinks, UsefulLinksMenu]:

                for field in model._meta.get_fields():
                    field_str = field.get_attname()
                    for item in model.objects.all():
                        msgid = "%s.%s.%s." % (item._meta, item.pk, field_str)
                        msgval = getattr(item, field_str)
                        if isinstance(msgval, StreamValue):
                            msg_data = msgval.stream_data
                            path_dict = {}
                            original_path = ""
                            path_dict = generate_json_paths(msg_data, original_path, path_dict)
                            for tr_field in path_dict.keys():
                                if tr_field[-3:] == "_%s" % lang:
                                    en_field = "%s_en" % tr_field[:-3]
                                    enstr = fetch_json_by_path(msg_data, en_field)
                                    if enstr is not None:
                                        msgstr = fetch_json_by_path(msg_data, en_field)
                                        if msgstr is None:
                                            msgstr = ""
                                        to_translate.append(
                                            {
                                                "enstr": enstr,
                                                "msgstr": msgstr,
                                                "msgid": msgid + en_field
                                            }
                                        )
                        else:
                            if field_str[-3:] == "_%s" % lang:
                                en_field = "%s_en" % field_str.split("_")[0]
                                if hasattr(model, en_field):
                                    enval = getattr(item, en_field)
                                    if msgval is not None:
                                        msgstr = "%s" % msgval
                                    else:
                                        msgstr = ""
                                    if enval is not None:
                                        enstr = "%s" % enval
                                        to_translate.append(
                                            {
                                                "enstr": enstr,
                                                "msgstr": msgstr,
                                                "msgid": msgid
                                            }
                                        )

            for translation_obj in to_translate:
                enstr = translation_obj["enstr"]
                msgstr = translation_obj["msgstr"]
                msgid = translation_obj["msgid"]
                # We already have a translation, just add the new comment to pick it up
                if enstr in existing_ids:
                    catalog.add(id=enstr, string=msgstr, auto_comments=[msgid, ])
                # We don't have an exact translation, but we've translated the page before
                elif msgid in existing_trans.keys():
                    # It's not JSON, just add it. We can't delete because can't guarantee it's not reused later
                    catalog.add(id=enstr, string=msgstr, auto_comments=[msgid, ])
                    word_count += len(enstr.split())
                # If we don't have a translation, and it's not in a previously translated page, it's brand new
                else:
                    catalog.add(id=enstr, string=msgstr, auto_comments=[msgid, ])
                    word_count += len(enstr.split())

            # write catalog to file
            po_file = open(po_filepath, "wb")
            write_po(po_file, catalog, width=None)
            po_file.close()
            print("New {} word count: {}".format(lang, word_count))
