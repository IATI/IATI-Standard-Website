"""Management command that fixes invalid json savedin content editors in .po file."""

import json
from os.path import isdir, join

from babel.messages.pofile import read_po, write_po
from django.conf import settings
from django.core.management.base import BaseCommand as LoadCommand
from django.core.management.base import CommandError


def repair_json(s):
    """Find and replace invalid json characters."""
    try:
        json.loads(s)
    except json.JSONDecodeError as e:
        original_string = s
        start = e.pos
        end = s.find("]", start) + 1
        part_to_replace = s[start:end - 3]
        escaped = part_to_replace.replace('"', r'\"')
        final_escaped = escaped.replace('\n', '')
        final_string = original_string[:start] + final_escaped + original_string[-3:]
        return final_string


class Command(LoadCommand):
    """Management command that fixes invalid json in content editors in .po file."""

    def add_arguments(self, parser):
        """Add custom command arguments."""
        parser.add_argument('pks', nargs='+', type=int)

    def handle(self, *args, **options):
        """Handle method for fix_json command."""
        locale_path = settings.MODELTRANSLATION_LOCALE_PATH
        po_file_name = "iati.po"
        if not isdir(locale_path):
            raise CommandError("Locale directory does not exists.")
        french_file_path = join(locale_path, 'fr')
        if not isdir(french_file_path):
            raise CommandError("Language directory does not exist.")

        po_file = open(join(french_file_path, "LC_MESSAGES", po_file_name), "r", encoding="utf-8")
        catalog = read_po(po_file)
        po_file.close()
        for message in catalog:
            if message.string not in [None, "None", ""] and message.auto_comments:
                for field_id in message.auto_comments:
                    [app, class_name, primary_key, field] = field_id.split('.')
                    if int(primary_key) in options['pks'] and app == "news" and field == "content_editor":
                        message.string = repair_json(message.string.strip())
                        po_file = open(join(french_file_path, "LC_MESSAGES", po_file_name), "wb")
                        write_po(po_file, catalog, width=None)
                        po_file.close()
