# pylint: disable=too-many-locals, duplicate-code
"""Management command that loads locale .po files into database."""

from __future__ import unicode_literals
from os.path import join, isdir
from django.conf import settings

from django.core.management.base import BaseCommand as LoadCommand, CommandError
from django.apps import apps
from babel.messages.pofile import read_po
from .save_trans import load_translation_settings


class Command(LoadCommand):
    """Management command that loads locale .po files into database."""

    def handle(self, *args, **options):
        """Handle the load_trans command."""
        po_filename = load_translation_settings(settings)
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
                            [app, class_name, primary_key, field] = field_id.split('.')
                            model = apps.get_model(app, class_name)
                            try:
                                obj = model.objects.get(pk=primary_key)
                            except model.DoesNotExist:
                                continue
                            tr_field = "%s_%s" % (field, lang)
                            setattr(obj, tr_field, message.string)
                            obj.save()
