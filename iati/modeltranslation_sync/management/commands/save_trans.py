# pylint: disable=too-many-locals, too-many-branches, duplicate-code
"""Management command that saves locale .po files from database."""

from __future__ import unicode_literals
import json
from os import mkdir
from os.path import join, isdir

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from modeltranslation.translator import translator
from babel.messages.catalog import Catalog
from babel.messages.pofile import write_po


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


class Command(BaseCommand):
    """Management command that saves locale .po files from database."""

    def handle(self, *args, **options):
        """Handle the save_trans command."""
        filename_po = load_translation_settings(settings)

        locale_path = settings.MODELTRANSLATION_LOCALE_PATH
        if not isdir(locale_path):
            mkdir(locale_path)

        for lang in [l[0] for l in list(settings.LANGUAGES)]:

            catalog = Catalog(locale=lang)

            for model in translator.get_registered_models():
                opts = translator.get_options_for_model(model)

                for field in opts.get_field_names():
                    tr_field = "%s_%s" % (field, lang)
                    en_field = "%s_%s" % (field, "en")
                    for item in model.objects.all():
                        msgid = "%s.%s.%s" % (item._meta, item.pk, field)
                        msgstr = "%s" % getattr(item, tr_field)
                        enval = getattr(item, en_field)
                        if enval is not None and field not in ["slug", "url_path"]:
                            enstr = json.dumps(enval.stream_data) if hasattr(enval, "stream_data") else "%s" % enval
                            catalog.add(id=enstr, string=msgstr, auto_comments=[msgid, ])

            # write catalog to file
            lang_path = join(locale_path, lang)
            if not isdir(lang_path):
                mkdir(lang_path)
                mkdir(join(lang_path, "LC_MESSAGES"))
            po_file = open(join(lang_path, "LC_MESSAGES", filename_po), "wb")
            write_po(po_file, catalog)
            po_file.close()
