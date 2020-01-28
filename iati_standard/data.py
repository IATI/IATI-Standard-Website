"""Module for handling IATI standard reference data."""
import requests
import io
import os
import json
from zipfile import ZipFile
from django.conf import settings
from django.utils.text import slugify
from iati_standard.models import ReferenceData, ActivityStandardPage, IATIStandardPage
from iati_standard.edit_handlers import GithubAPI


def download_zip(url):
    """Download a ZIP file."""
    headers = {
        'Authorization': 'token %s' % settings.GITHUB_TOKEN,
        'Accept': 'application/octet-stream',
    }
    response = requests.get(url, headers=headers)
    return ZipFile(io.BytesIO(response.content))


def extract_zip(zipfile):
    """Extract zip in memory and yields (filename, file-like object) pairs."""
    with zipfile as thezip:
        for zipinfo in thezip.infolist():
            with thezip.open(zipinfo) as thefile:
                if not zipinfo.filename.startswith('.') and not zipinfo.filename.startswith('__MACOSX') and not zipinfo.is_dir():
                    yield thefile


def update_or_create_tags(observer, repo, tag=None):
    """Create or update tags."""
    observer.update_state(
        state='PROGRESS',
        meta='Retrieving data and media from Github'
    )
    git = GithubAPI(repo)

    if tag:
        data = git.get_data(tag)

        populate_data(observer, data, tag)
        populate_index(observer, tag)

        observer.update_state(
            state='PROGRESS',
            meta='All tasks complete'
        )

    return True


def populate_data(observer, data, tag):
    """Use ZIP data to create reference data objects."""
    observer.update_state(
        state='PROGRESS',
        meta='Data retrieved, updating database'
    )

    if data:
        for item in extract_zip(download_zip(data.url)):
            if os.path.splitext(item.name)[1] == ".json":
                try:
                    raw_json_path = os.path.splitext(item.name)[0]
                    version = raw_json_path.split("/")[1]
                    language = raw_json_path.split("/")[2]
                    if language in [lang[0] for lang in settings.ACTIVE_LANGUAGES]:
                        path_remainder = "/".join(raw_json_path.split("/")[3:])
                        json_path = "/".join([version, path_remainder])
                        ReferenceData.objects.update_or_create(
                            json_path=json_path,
                            version=version,
                            language=language,
                            tag=tag,
                            defaults={'data': json.loads(item.read())},
                        )
                except json.decoder.JSONDecodeError:
                    pass

    else:
        raise ValueError('No data available for tag: %s' % tag)


def create_or_update_from_object(parent_page, page_model, object):
    """Create ActivityStandardPage from ReferenceData object."""
    try:
        child_page = page_model.objects.get(
            json_path=object.json_path
        )
        setattr(child_page, "data_{}".format(object.language), object.data)
        child_page.tag = object.tag
        child_page.save_revision().publish()
    except page_model.DoesNotExist:
        child_page = page_model(
            json_path=object.json_path,
            title=object.name,
            heading=object.name,
            slug=slugify(object.name),
            tag=object.tag
        )
        setattr(child_page, "data_{}".format(object.language), object.data)
        parent_page.add_child(instance=child_page)
        child_page.save_revision().publish()
    return child_page


def recursive_create(ancestor_list, object_pool, parent_page, parent_path):
    """Recursively create ActivityStandardPage objects."""
    objects = object_pool.filter(parent_path=parent_path)
    for object in objects:
        if object.reference_type in ancestor_list:
            page_model = ActivityStandardPage
            child_page = create_or_update_from_object(parent_page, page_model, object)
            if not child_page.has_been_recursed:
                child_page.has_been_recursed = True
                child_page.save_revision().publish()
                recursive_create(ancestor_list, object_pool, child_page, child_page.json_path)
    return True


def populate_index(observer, tag, previous_tag=None):
    """Use ReferenceData objects to populate page index."""
    observer.update_state(
        state='PROGRESS',
        meta='Populating index'
    )

    versions = [vers[0] for vers in ReferenceData.objects.filter(tag=tag).order_by().values_list('version').distinct()]
    ActivityStandardPage.objects.all().update(has_been_recursed=False)

    for version in versions:
        standard_page = IATIStandardPage.objects.live().first()
        objects = ReferenceData.objects.filter(tag=tag, json_path="{}/activity-standard".format(version))
        for object in objects:
            version_page = create_or_update_from_object(standard_page, ActivityStandardPage, object)
        version_page.title = version
        version_page.slug = slugify(version)
        version_page.save_revision().publish()
        ancestor_list = [
            "activity-standard"
        ]
        recursive_create(ancestor_list, ReferenceData.objects.filter(tag=tag), version_page, version_page.json_path)

    if previous_tag:
        new_object_paths = set(ReferenceData.objects.filter(tag=tag).order_by().values_list('json_path'))
        old_object_paths = set(ReferenceData.objects.filter(tag=previous_tag).order_by().values_list('json_path'))

        to_delete = (old_object_paths - new_object_paths)
        ActivityStandardPage.objects.filter(json_path__in=list(to_delete)).delete()
