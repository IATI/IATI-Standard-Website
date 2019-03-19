from django.urls import reverse
from wagtail.images.views.serve import generate_signature


def generate_image_url(image, filter_spec='original'):
    """Return generated URL for image."""
    signature = generate_signature(image.id, filter_spec)
    url = reverse('wagtailimages_serve', urlconf='wagtail.images.urls', args=(signature, image.id, filter_spec))
    return url
