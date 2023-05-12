# pylint: disable=too-many-locals, duplicate-code
"""Management command that copies translations from .po files into relevant pages."""

from __future__ import unicode_literals
from os.path import join, isdir
from django.conf import settings

from django.core.management.base import BaseCommand as LoadCommand, CommandError
from django.apps import apps
from babel.messages.pofile import read_po
from wagtail_localize.operations import translate_object
from wagtail.models import Locale


def load_translation_settings(django_settings):
    """Check app settings and load configuration for translation."""
    if not hasattr(django_settings, 'MODELTRANSLATION_LOCALE_PATH'):
        raise CommandError("Settings has no attribute 'MODELTRANSLATION_LOCALE_PATH'")

    if not hasattr(django_settings, 'MODELTRANSLATION_PO_FILE'):
        filename_po = "modeltranslation.po"
    else:
        filename_po = settings.MODELTRANSLATION_PO_FILE
        if not filename_po.endswith(".po"):
            filename_po += '.po'
    return filename_po

class Command(LoadCommand):
    """Management command that copies translations from .po files into relevant pages."""

    # def add_arguments(self, parser):
    #     """Add custom command arguments."""
    #     parser.add_argument('pks', nargs='*', type=int)

    def handle(self, *args, **options):
        """Handle the apply translations command."""
        po_filename = load_translation_settings(settings)
        locale_path = settings.MODELTRANSLATION_LOCALE_PATH
        
        if not isdir(locale_path):
            raise CommandError("Locale directory does not exists.")
        for lang in [lang_tup[0] for lang_tup in list(settings.LANGUAGES)]:
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
                            translate_object(obj,[Locale.objects.get(language_code='fr')])
                            print('Translating')
                            print(obj)
                            print('Done')


