# pylint: disable=too-many-locals, duplicate-code
"""Management command that fixes malformed content editors in .po file"""

from __future__ import unicode_literals
from os.path import join, isdir
from django.conf import settings

from django.core.management.base import BaseCommand as LoadCommand, CommandError
from babel.messages.pofile import read_po, write_po
from .save_trans import load_translation_settings

from bs4 import BeautifulSoup
import json


class Command(LoadCommand):
    """Management command that fixes malformed content editors in .po file"""

    def add_arguments(self, parser):
        """Add custom command arguments."""
        parser.add_argument('pks', nargs='+', type=int)

    def handle(self, *args, **options):
        """Handle the fix_malformed command."""
        po_filename = load_translation_settings(settings)
        locale_path = settings.MODELTRANSLATION_LOCALE_PATH
        if not isdir(locale_path):
            raise CommandError("Locale directory does not exists.")
        lang = "fr"
        lang_path = join(locale_path, lang)
        if not isdir(lang_path):
            raise CommandError("Language directory does not exists.")
        po_file = open(join(lang_path, "LC_MESSAGES", po_filename), "r", encoding="utf-8")
        catalog = read_po(po_file)
        po_file.close()
        for message in catalog:
            if message.string not in [None, "None", ""] and message.auto_comments:
                for field_id in message.auto_comments:
                    [app, class_name, primary_key, field] = field_id.split('.')
                    if int(primary_key) in options['pks'] and field == "content_editor":
                        parsed_json = json.loads(message.string)
                        for field in parsed_json:
                            if field["type"] == "paragraph":
                                field["value"] = str(BeautifulSoup(field["value"], "html.parser").prettify())
                        message.string = json.dumps(parsed_json)
        po_file = open(join(lang_path, "LC_MESSAGES", po_filename), "wb")
        write_po(po_file, catalog, width=None)
        po_file.close()
