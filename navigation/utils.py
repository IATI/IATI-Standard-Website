"""Module of utilities for navigation."""

from django.utils.translation import get_language
from django.conf import settings


def get_field_value(instance, field_name, use_get):
    """Get a field value given an instance."""
    if use_get:
        field_value = instance.get(field_name)
    else:
        field_value = getattr(instance, field_name, '')
    return field_value


def get_localised_field_value(instance, field_name, use_get=False):
    """Get a localised field value given an instance."""
    try:
        current_language = get_language()
        default_language = settings.LANGUAGES[0][0]

        current_field_name = '%s_%s' % (field_name, current_language)
        default_field_name = '%s_%s' % (field_name, default_language)

        field_value = get_field_value(instance, current_field_name, use_get)
        if (field_value):  # noqa
            return field_value

        if current_field_name != default_field_name:
            field_value = get_field_value(instance, default_field_name, use_get)
            if (field_value):  # noqa
                return field_value

        return ''

    except Exception:
        return ''


def get_default_lang_slug(instance):
    """Get the default language slug."""
    try:
        default_language = settings.LANGUAGES[0][0]
        slug_name = 'slug_%s' % default_language
        return getattr(instance, slug_name, '')

    except Exception:
        return ''
