import io
import urllib3
import os.path
from django.conf import settings
from django.core.files.images import ImageFile
from django.db.models import Q
from wagtail.images import get_image_model


def delete_existing_file(filename, folder):
    """Delete an existing file."""
    destination = '%s/%s/' % (settings.MEDIA_ROOT, folder)
    path = destination + filename
    if os.path.isfile(path):
        os.remove(path)


def get_file_from_url(url):
    """Get a file from a URL."""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager()
    data = None
    response = http.request('GET', url, preload_content=False)
    if response.status == 200:
        data = io.BytesIO(response.read())
    return data


def get_or_create_image(url, title=None):
    """Get or create an image."""
    Image = get_image_model()
    filename = url.rsplit('/', 1)[1]
    image = Image.objects.filter(Q(title=filename) | Q(title=title)).first()

    if image and title:
        image.title = title
        image.save()

    if not image:
        try:
            image_obj = get_file_from_url(url)
            if title:
                title = title[:255]
            else:
                filename = filename[:255]
            if image_obj:
                delete_existing_file(filename, 'original_images')
                image_file = ImageFile(image_obj, name=filename)
                image = Image(
                    title=title or filename,
                    file=image_file,
                )
                image.save()
        except Exception:
            pass

    return image


def get_field_value(obj, instance, column):
    """Get a field value from an object."""
    fields = obj.get_fields()
    for field in fields:
        if field.column_name == column:
            return field.get_value(instance)
    return None
