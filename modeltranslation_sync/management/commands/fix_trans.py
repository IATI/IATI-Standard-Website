# pylint: disable=too-many-locals, duplicate-code
"""Management command that fixes locale .po files."""

from __future__ import unicode_literals
from os.path import join, isdir
import json
import html

from bs4 import BeautifulSoup

from wagtail.documents.models import Document
from wagtail.images.models import Image

from django.conf import settings
from django.core.management.base import BaseCommand as LoadCommand, CommandError

from babel.messages.pofile import read_po, write_po

from .save_trans import load_translation_settings


def find_image_pk(image_key, subelement_dict, field_id):
    """Small function to find an image PK, given a dictionary and key."""
    if image_key in subelement_dict.keys():
        image_name = html.unescape(subelement_dict[image_key].decode_contents())
        img_check = Image.objects.filter(title=image_name)
        if img_check:
            return img_check.first().pk
        print("ERR: Unable to serialize image {} from {}".format(image_name, field_id))
    return None


class Command(LoadCommand):
    """Management command that fixes locale .po files."""

    def handle(self, *args, **options):
        """Handle the load_trans command."""
        po_filename = load_translation_settings(settings)
        locale_path = settings.MODELTRANSLATION_LOCALE_PATH
        if not isdir(locale_path):
            raise CommandError("Locale directory does not exists.")
        for lang in [lang_tup[0] for lang_tup in list(settings.LANGUAGES)]:
            if lang != "en":
                lang_path = join(locale_path, lang)
                if not isdir(lang_path):
                    raise CommandError("Language directory does not exists.")
                po_file = open(join(lang_path, "LC_MESSAGES", po_filename), "r")
                catalog = read_po(po_file)
                po_file.close()
                for message in catalog:
                    if message.string not in [None, "None", ""] and message.auto_comments and message.string[0] != "[":
                        field_id = message.auto_comments[0]
                        [app, class_name, primary_key, field] = field_id.split('.')
                        message_json = []
                        culprit = False
                        if field == 'content_editor':
                            soup = BeautifulSoup(message.string, "html.parser")
                            for child_elem in soup.findAll("div", recursive=False):
                                if "block-h2" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    json_obj = {"type": "h2", "value": child_elem.decode_contents()}
                                    message_json.append(json_obj)
                                if "block-h3" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    json_obj = {"type": "h3", "value": child_elem.decode_contents()}
                                    message_json.append(json_obj)
                                if "block-h4" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    json_obj = {"type": "h4", "value": child_elem.decode_contents()}
                                    message_json.append(json_obj)
                                if "block-intro" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    richText = child_elem.find("div", {"class": "rich-text"})
                                    json_obj = {"type": "intro", "value": richText.decode_contents()}
                                    message_json.append(json_obj)
                                if "block-paragraph" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    richText = child_elem.find("div", {"class": "rich-text"})
                                    try:
                                        json_obj = {"type": "paragraph", "value": richText.decode_contents()}
                                    except AttributeError:
                                        json_obj = {"type": "paragraph", "value": child_elem.decode_contents()}
                                    message_json.append(json_obj)
                                if "block-image_figure" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    subelements = child_elem.findAll("dd")
                                    subelement_keys = child_elem.findAll("dt")
                                    subelement_dict = {}
                                    for i in range(0, len(subelement_keys)):
                                        subelement = subelements[i]
                                        subelement_key = subelement_keys[i].decode_contents()
                                        subelement_dict[subelement_key] = subelement
                                    image_name = html.unescape(subelement_dict["image"].decode_contents())
                                    image_alignment = subelement_dict["alignment"].decode_contents()
                                    caption = subelement_dict["caption"].find("div", {"class": "rich-text"}).decode_contents()
                                    img_check = Image.objects.filter(title=image_name)
                                    if img_check:
                                        image_pk = img_check.first().pk
                                        json_obj = {
                                            "type": "image_figure", "value": {
                                                "alignment": image_alignment,
                                                "caption": caption,
                                                "image": image_pk
                                            }
                                        }
                                        message_json.append(json_obj)
                                    else:
                                        print("ERR: Unable to serialize image {} from {}".format(image_name, field_id))
                                if "block-pullquote" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    richText = child_elem.find("dd")
                                    json_obj = {"type": "pullquote", "value": {"quote": richText.decode_contents()}}
                                    message_json.append(json_obj)
                                if "block-aligned_html" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    subelements = child_elem.findAll("dd")
                                    subelement_keys = child_elem.findAll("dt")
                                    subelement_dict = {}
                                    for i in range(0, len(subelement_keys)):
                                        subelement = subelements[i]
                                        subelement_key = subelement_keys[i].decode_contents()
                                        subelement_dict[subelement_key] = subelement
                                    json_obj = {
                                        "type": "aligned_html", "value": {
                                            "alignment": subelement_dict["alignment"].decode_contents(),
                                            "html": subelement_dict["html"].decode_contents()
                                        }
                                    }
                                    message_json.append(json_obj)
                                if "block-document_box" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    try:
                                        heading = child_elem.find("div", {"class": "block-document_box_heading"}).decode_contents()
                                    except AttributeError:
                                        heading = ""
                                    json_obj = {
                                        "type": "document_box", "value": [
                                            {"type": "document_box_heading", "value": heading}
                                        ]
                                    }
                                    documents = child_elem.findAll("div", {"class": "block-document"})
                                    for document in documents:
                                        doc_anchor = document.find("a")
                                        try:
                                            doc_name = html.unescape(doc_anchor.decode_contents())
                                        except AttributeError:
                                            doc_name = None
                                        doc_check = Document.objects.filter(title=doc_name)
                                        if doc_check:
                                            doc_pk = doc_check.first().pk
                                            json_obj["value"].append({"type": "document", "value": doc_pk})
                                        else:
                                            print("ERR: Unable to serialize document {} from {}".format(doc_name, field_id))
                                    message_json.append(json_obj)
                                if "block-anchor_point" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    json_obj = {"type": "anchor_point", "value": child_elem.decode_contents()}
                                    message_json.append(json_obj)
                        if field == 'timeline_editor':
                            soup = BeautifulSoup(message.string, "html.parser")
                            for child_elem in soup.findAll("div", recursive=False):
                                if "block-event_block_editor" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    subelements = child_elem.findAll("dd")
                                    subelement_keys = child_elem.findAll("dt")
                                    subelement_dict = {}
                                    for i in range(0, len(subelement_keys)):
                                        subelement = subelements[i]
                                        subelement_key = subelement_keys[i].decode_contents()
                                        subelement_dict[subelement_key] = subelement
                                    json_obj = {
                                        "type": "event_block_editor", "value": {
                                            "heading": subelement_dict["heading"].decode_contents(),
                                            "description": subelement_dict["description"].decode_contents()
                                        }
                                    }
                                    message_json.append(json_obj)
                        if field == 'profile_content_editor':
                            soup = BeautifulSoup(message.string, "html.parser")
                            for child_elem in soup.findAll("div", recursive=False):
                                if "block-section_heading" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    json_obj = {"type": "section_heading", "value": child_elem.decode_contents()}
                                    message_json.append(json_obj)
                                if "block-paragraph" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    json_obj = {"type": "paragraph", "value": child_elem.decode_contents()}
                                    message_json.append(json_obj)
                                if "block-pullquote" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    richText = child_elem.find("dd")
                                    json_obj = {"type": "pullquote", "value": {"quote": richText.decode_contents()}}
                                    message_json.append(json_obj)
                                if "block-profile_editor" == child_elem.attrs["class"][0]:
                                    culprit = True
                                    subelements = child_elem.findAll("dd")
                                    subelement_keys = child_elem.findAll("dt")
                                    subelement_dict = {}
                                    for i in range(0, len(subelement_keys)):
                                        subelement = subelements[i]
                                        subelement_key = subelement_keys[i].decode_contents()
                                        subelement_dict[subelement_key] = subelement
                                    json_obj = {
                                        "type": "profile_editor", "value": {
                                            "name": subelement_dict["name"].decode_contents(),
                                            "profile_picture": find_image_pk("profile_picture", subelement_dict, field_id),
                                            "organisation_logo": find_image_pk("organisation_logo", subelement_dict, field_id),
                                            "organisation_name": subelement_dict["organisation_name"].decode_contents(),
                                            "IATI_role": subelement_dict["IATI_role"].decode_contents(),
                                            "external_role": subelement_dict["external_role"].decode_contents(),
                                            "description": subelement_dict["description"].decode_contents(),
                                            "IATI_constituency": subelement_dict["IATI_constituency"].decode_contents()
                                        }
                                    }
                                    message_json.append(json_obj)
                        if culprit:
                            message.string = json.dumps(message_json, ensure_ascii=False)
                po_file = open(join(lang_path, "LC_MESSAGES", po_filename), "wb")
                write_po(po_file, catalog, width=None)
                po_file.close()
