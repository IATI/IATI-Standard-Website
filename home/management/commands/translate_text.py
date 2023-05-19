# pylint: disable=too-many-locals, duplicate-code
"""Management command that copies translations from .po files into relevant pages."""

from __future__ import unicode_literals

import re
import json
import polib
import tempfile
import requests
import urllib
from bs4 import BeautifulSoup
from os.path import join, isdir

from django.conf import settings
from django.core.management.base import BaseCommand as LoadCommand, CommandError
from django.apps import apps
from django.http import Http404, HttpResponse
from django.utils.text import slugify
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError

from babel.messages.pofile import read_po

from wagtail_localize.operations import translate_object
from wagtail.models import Locale
from wagtail_localize.models import (
    Translation
)
from wagtail_localize.synctree import PageIndex
from wagtail_localize.models import Translation
from wagtail_localize.operations import translate_object


def find_string(needle, haystack):
    return [m.start() for m in re.finditer(needle, haystack)]

def create_translation_pages():
    source_locale = Locale.objects.get(language_code='en')
    target_locale = Locale.objects.get(language_code='fr')
    page_index = PageIndex.from_database().sort_by_tree_position()
    pages_in_locale = [page for page in page_index if source_locale.id in page.locales]

    for page in pages_in_locale:
        model = page.content_type.model_class()
        source_page = model.objects.get(translation_key=page.translation_key, locale=source_locale)

        try:
            translate_object(source_page, [target_locale])
        except Exception as e:
            print(source_page)

def translate_pages():
    translation_pages = Translation.objects.all()
    for translation_page in translation_pages:
        downloaded_filename = download_po_file(translation_page)
        updated_file = add_translations_to_pofile(downloaded_filename)
        updated_file[1].save()
        upload_po_file(updated_file[0], translation_page)
    return downloaded_filename

def find_language_translation_in_iati_po_file(text_to_translate, field_reference):
    field_reference_parts = field_reference.split(".")
    count = len(field_reference_parts)
    locale_path = settings.MODELTRANSLATION_LOCALE_PATH
    po = polib.pofile(join(locale_path, "fr", "LC_MESSAGES", "iati.po"))
    for entry in po:
        if count > 1:            
            result = find_string(field_reference_parts[count - 1], entry.msgstr)
            if len(result):
                data = json.loads(entry.msgstr)
                for x in data:
                    if x['id'] == field_reference_parts[count - 1]:
                        print('x')
                        return x['value']
        else:
            soup_for_text_to_translate = BeautifulSoup(text_to_translate, features="html.parser")
            soup_for_iati_text = BeautifulSoup(entry.msgid, features="html.parser")
            if soup_for_text_to_translate.get_text() == soup_for_iati_text.get_text():
                print('y')
                return entry.msgstr
        
    return ""

def add_translations_to_pofile(filename):
    po = polib.pofile(join(settings.MODELTRANSLATION_LOCALE_PATH, filename))
    for entry in po:
        translated_text = find_language_translation_in_iati_po_file(entry.msgid, entry.msgctxt)
        print("text to translate")
        print(entry.msgid)
        print(entry.msgctxt)
        print('_______________________________________________________________')
        print("translated text")
        print(translated_text)
        print('_______________________________________________________________')
        if translated_text:
            entry.msgstr = translated_text
            # print('Translated ' + entry.msgid)
        # else:
            # print('Cannot Translate ' + entry.msgid)
    return (filename, po)

def download_po_file(translation_instance):
    response = HttpResponse(
        str(translation_instance.export_po()), content_type="text/x-gettext-translation"
    )
    filename = "{}-{}.po".format(
        slugify(translation_instance.source.object_repr),
        translation_instance.target_locale.language_code,
    )
    with open(join(settings.MODELTRANSLATION_LOCALE_PATH, filename), "wb") as f:
        f.write(response.content)
    
    return filename

def upload_po_file(filename, translation):
    do_import = True
    with tempfile.NamedTemporaryFile() as f:
        # Note: polib.pofile accepts either a filename or contents. We cannot pass the
        # contents directly into polib.pofile or users could upload a file containing
        # a filename and this will be read by polib!
        f.write(open(join(settings.MODELTRANSLATION_LOCALE_PATH, filename), 'rb').read())
        f.flush()

        try:
            po = polib.pofile(f.name)

        except (OSError, UnicodeDecodeError):
            # Annoyingly, POLib uses OSError for parser exceptions...
            print("Please upload a valid PO file.")
            do_import = False

    if do_import:
        translation_id = po.metadata["X-WagtailLocalize-TranslationID"]
        if translation_id != str(translation.uuid):
            print("Cannot import PO file that was created for a different translation.")
            do_import = False

    if do_import:
        translation.import_po(po, tool_name="PO File")

        print("Successfully imported translations from PO File.")


class Command(LoadCommand):
    """Management command that translates the pages from English to any given language using .po files."""

    def handle(self, *args, **options):

        # Create translation pages in the wagtail editor
        create_translation_pages()

        # Apply translations using po files
        translate_pages()

        



