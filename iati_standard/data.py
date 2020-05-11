"""Module for handling IATI standard reference data."""
import requests
import io
import os
from zipfile import ZipFile
from django.conf import settings
from django.utils.text import slugify
from wagtail.core.models import Page
from iati_standard.models import ReferenceData, ActivityStandardPage, IATIStandardPage, ReferenceMenu, StandardGuidanceIndexPage, StandardGuidancePage
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


def update_or_create_tags(observer, repo, tag=None, guidance_parent_page=None):
    """Create or update tags."""
    observer.update_state(
        state='PROGRESS',
        meta='Retrieving data and media from Github'
    )
    git = GithubAPI(repo)

    if tag:
        data = git.get_data(tag)

        populate_data(observer, data, tag)
        populate_index(observer, tag, guidance_parent_page)

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
            if os.path.splitext(item.name)[1] == ".html":
                ssot_path = os.path.dirname(item.name)
                ReferenceData.objects.update_or_create(
                    ssot_path=ssot_path,
                    tag=tag,
                    defaults={'data': item.read().decode('utf-8').replace("\n", "")},
                )

    else:
        raise ValueError('No data available for tag: %s' % tag)


def create_or_update_from_object(parent_page, page_model, object):
    """Create ActivityStandardPage from ReferenceData object."""
    try:
        child_page = page_model.objects.get(
            ssot_path=object.ssot_path
        )
        setattr(child_page, "data_{}".format(object.language), object.data)
        child_page.tag = object.tag
        child_page.locked = True
        child_page.locked_by = None
        child_page.save_revision().publish()
    except page_model.DoesNotExist:
        child_page = page_model(
            ssot_path=object.ssot_path,
            title=object.name,
            heading=object.name,
            slug=slugify(object.name),
            tag=object.tag
        )
        setattr(child_page, "data_{}".format(object.language), object.data)
        child_page.locked = True
        child_page.locked_by = None
        parent_page.add_child(instance=child_page)
        child_page.save_revision().publish()
    return child_page


def recursive_create(object_pool, parent_page, parent_path, recursed_page_paths):
    """Recursively create ActivityStandardPage objects."""
    objects = object_pool.filter(parent_path=parent_path)
    for object in objects:
        page_model = ActivityStandardPage
        child_page = create_or_update_from_object(parent_page, page_model, object)
        if child_page.ssot_path not in recursed_page_paths:
            recursed_page_paths.append(child_page.ssot_path)
            recursive_create(object_pool, child_page, child_page.ssot_path, recursed_page_paths)
    return True


def recursive_create_menu(parent_page):
    """Recursively create reference menu."""
    page_obj = {
        "depth": parent_page.depth,
        "title": parent_page.title,
        "pk": parent_page.pk,
        "children": list()
    }
    page_children = parent_page.get_children()
    if len(page_children) == 0:
        return page_obj
    for page_child in page_children:
        page_obj["children"].append(
            recursive_create_menu(page_child)
        )
    return page_obj


def populate_index(observer, tag, guidance_parent_page=None):
    """Use ReferenceData objects to populate page index."""
    observer.update_state(
        state='PROGRESS',
        meta='Populating index'
    )

    new_object_paths = set(ReferenceData.objects.filter(tag=tag).order_by().values_list('ssot_path'))
    old_object_paths = set(ReferenceData.objects.exclude(tag=tag).order_by().values_list('ssot_path'))

    to_delete = [item[0] for item in (old_object_paths - new_object_paths)]
    ActivityStandardPage.objects.filter(ssot_path__in=list(to_delete)).delete()

    ssot_roots = [roots[0] for roots in ReferenceData.objects.filter(tag=tag).order_by().values_list('ssot_root_slug').distinct()]
    recursed_page_paths = []
    menu_json = []

    for ssot_root in ssot_roots:
        standard_page = IATIStandardPage.objects.live().first()
        if ssot_root != 'guidance':
            objects = ReferenceData.objects.filter(tag=tag, ssot_path=ssot_root)
            for object in objects:
                ssot_root_page = create_or_update_from_object(standard_page, ActivityStandardPage, object)
            ssot_root_page.title = ssot_root
            ssot_root_page.slug = slugify(ssot_root)
            ssot_root_page.save_revision().publish()
        else:
            if guidance_parent_page:
                standard_page = Page.objects.get(pk=guidance_parent_page).specific
                ssot_root_page = StandardGuidanceIndexPage.objects.live().descendant_of(standard_page)
                if not ssot_root_page:
                    ssot_root_page = StandardGuidanceIndexPage(
                        title="Standard Guidance",
                        heading="Standard Guidance",
                        slug="standard-guidance"
                    )
                    ssot_root_page.locked = True
                    ssot_root_page.locked_by = None
                    standard_page.add_child(instance=ssot_root_page)
                    ssot_root_page.save_revision().publish()

        recursive_create(ReferenceData.objects.filter(tag=tag), ssot_root_page, ssot_root_page.ssot_path, recursed_page_paths)
        menu_json.append(recursive_create_menu(ssot_root_page))

        ReferenceMenu.objects.update_or_create(
            tag=tag,
            defaults={'menu_json': menu_json},
        )
