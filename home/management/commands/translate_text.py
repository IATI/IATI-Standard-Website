# pylint: disable=too-many-locals, duplicate-code
"""Management command that copies translations from .po files into relevant pages."""

from __future__ import unicode_literals

import re
import json
import polib
import tempfile
from os.path import join

from django.conf import settings
from django.core.management.base import BaseCommand as LoadCommand, CommandError
from django.apps import apps
from django.http import HttpResponse
from django.utils.text import slugify

from babel.messages.pofile import read_po

from wagtail.models import Page
from wagtail.models import Locale
from wagtail.blocks.stream_block import StreamValue
from wagtail_localize.operations import translate_object
from wagtail_localize.synctree import PageIndex
from wagtail_localize.models import Translation, TranslationSource


def build_old_po_file_dict():
    results = dict()
    all_locales = Locale.objects.all()
    lang_path = settings.MODELTRANSLATION_LOCALE_PATH
    for locale in all_locales:
        if locale.language_code != 'en':
            po_file = open(join(lang_path, locale.language_code, "LC_MESSAGES", "iati.po"), "r", encoding="utf-8")
            catalog = read_po(po_file)
            po_file.close()
            for message in catalog:
                if message.string not in [None, "None", ""] and message.auto_comments:
                    for field_id in message.auto_comments:
                        [app, class_name, primary_key, field] = field_id.split('.')
                        if app != 'wagtailcore':
                            model = apps.get_model(app, class_name)
                            try:
                                obj = model.objects.get(pk=primary_key)
                            except model.DoesNotExist:
                                continue
                            field_obj = getattr(obj, field)
                            if isinstance(field_obj, StreamValue):
                                stream_list = field_obj.raw_data
                                # print(type(stream_list))
                                for stream_item in stream_list:
                                    item_id = stream_item['id']
                                    item_values = stream_item['value']
                                    if not isinstance(item_values, dict):
                                        value_item_message_id = '{}.{}'.format(field, item_id)
                                        if locale.language_code not in results.keys():
                                            results[locale.language_code] = dict()
                                        if class_name not in results[locale.language_code].keys():
                                            results[locale.language_code][class_name] = dict()
                                        if primary_key not in results[locale.language_code][class_name].keys():
                                            results[locale.language_code][class_name][primary_key] = dict()
                                        results[locale.language_code][class_name][primary_key][value_item_message_id] = item_values
                                    else:
                                        for value_item_key, value_item_value in item_values.items():
                                            if not isinstance(value_item_value, dict):
                                                stream_value_item_message_id = '{}.{}.{}'.format(field, item_id, value_item_key)
                                                if locale.language_code not in results.keys():
                                                    results[locale.language_code] = dict()
                                                if class_name not in results[locale.language_code].keys():
                                                    results[locale.language_code][class_name] = dict()
                                                if primary_key not in results[locale.language_code][class_name].keys():
                                                    results[locale.language_code][class_name][primary_key] = dict()
                                                results[locale.language_code][class_name][primary_key][stream_value_item_message_id] = value_item_value
                                            else:
                                                print("WARNING: Stream depth too deep.")
                            else:
                                if locale.language_code not in results.keys():
                                    results[locale.language_code] = dict()
                                if class_name not in results[locale.language_code].keys():
                                    results[locale.language_code][class_name] = dict()
                                if primary_key not in results[locale.language_code][class_name].keys():
                                    results[locale.language_code][class_name][primary_key] = dict()
                                results[locale.language_code][class_name][primary_key][field] = message.string
    return results


def find_string(needle, haystack):
    return [m.start() for m in re.finditer(needle, haystack)]


def get_page_id(translation_page):
    translation_source = TranslationSource.objects.get(id=translation_page.source_id)
    content = json.loads(translation_source.content_json)
    return content['pk']


def get_classname(translation_page):
    translation_source = TranslationSource.objects.get(id=translation_page.source_id)
    content = json.loads(translation_source.content_json)
    page_object = Page.objects.get(pk=content['pk'])
    return page_object.specific._meta.model_name


def create_translation_pages(locale_code):
    source_locale = Locale.objects.get(language_code='en')
    try:
        target_locale = Locale.objects.get(language_code=locale_code)
    except Exception as e:
        raise CommandError('Target locale does not exist: ' + locale_code)

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
        updated_file = add_translations_to_pofile(downloaded_filename, translation_page)
        updated_file[1].save()
        upload_po_file(updated_file[0], translation_page)


results = build_old_po_file_dict()


def find_language_translation_in_iati_po_file(field_reference, translation_page):
    page_id = get_page_id(translation_page)
    page_id_string = str(page_id)
    locale = translation_page.target_locale.language_code
    class_name = get_classname(translation_page)
    if locale in results and class_name in results[locale] and page_id_string in results[locale][class_name] and field_reference in results[locale][class_name][page_id_string]:
        return results[locale][class_name][page_id_string][field_reference]
    else:
        return ""


def add_translations_to_pofile(filename, translation_page):
    locale = translation_page.target_locale.language_code
    lang_path = settings.MODELTRANSLATION_LOCALE_PATH
    po = polib.pofile(join(lang_path, locale, "LC_MESSAGES", filename))
    for entry in po:
        translated_text = find_language_translation_in_iati_po_file(entry.msgctxt, translation_page)
        if translated_text:
            entry.msgstr = translated_text
    return (filename, po)


def download_po_file(translation_instance):
    locale = translation_instance.target_locale.language_code
    lang_path = settings.MODELTRANSLATION_LOCALE_PATH
    filename = "{}-{}.po".format(
        slugify(translation_instance.source.object_repr),
        locale,
    )
    response = HttpResponse(
        str(translation_instance.export_po()), content_type="text/x-gettext-translation"
    )
    response["Content-Disposition"] = "attachment; filename={}".format(filename)
    with open(join(lang_path, locale, "LC_MESSAGES", filename), "wb") as f:
        f.write(response.content)

    return filename


def upload_po_file(filename, translation):
    locale = translation.target_locale.language_code
    lang_path = settings.MODELTRANSLATION_LOCALE_PATH
    with tempfile.NamedTemporaryFile() as f:
        # Note: polib.pofile accepts either a filename or contents. We cannot pass the
        # contents directly into polib.pofile or users could upload a file containing
        # a filename and this will be read by polib!
        f.write(open(join(lang_path, locale, "LC_MESSAGES", filename), 'rb').read())
        f.flush()

        try:
            po = polib.pofile(f.name)

        except (OSError, UnicodeDecodeError):
            # Annoyingly, POLib uses OSError for parser exceptions...
            print("Please upload a valid PO file.")
            raise CommandError('Please upload a valid PO file')

    translation_id = po.metadata["X-WagtailLocalize-TranslationID"]
    if translation_id != str(translation.uuid):
        print("Cannot import PO file that was created for a different translation.")
    else:
        translation.import_po(po, tool_name="PO File")
        print("Successfully imported translations from PO File: " + filename)


class Command(LoadCommand):
    """Management command that translates the pages from English to any given language using .po files."""
    def add_arguments(self, parser):
        """Add custom command arguments."""
        parser.add_argument('target_locale', nargs='?', type=str)

    def handle(self, *args, **options):
        if not options['target_locale']:
            raise CommandError('Please pass target locale as the first positional argument. eg. fr(French), es(Spanish)')

        # Create translation pages in the wagtail editor
        create_translation_pages(options['target_locale'])

        # Apply translations using po files
        translate_pages()
