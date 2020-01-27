from django.utils.translation import get_language
from django.conf import settings


def get_localised_field_value(instance, field_name, use_get=False):
    try:
        current_language = get_language()
        default_language = settings.LANGUAGES[0][0]

        current_field_name = '%s_%s' % (field_name, current_language)
        default_field_name = '%s_%s' % (field_name, default_language)

        if use_get:
            field_value = instance.get(current_field_name)
        else:
            field_value = getattr(instance, current_field_name, '')

        if field_value:
            return field_value

        elif current_field_name != default_field_name:
            if use_get:
                field_value = instance.get(default_field_name)
            else:
                field_value = getattr(instance, default_field_name, '')

            return field_value

        return ''

    except Exception as e:
        print(e)
        return ''


def get_default_lang_slug(instance):
    try:
        default_language = settings.LANGUAGES[0][0]
        slug_name = 'slug_%s' % default_language
        return getattr(instance, slug_name, '')

    except Exception as e:
        print(e)
        return ''
