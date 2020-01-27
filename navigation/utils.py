from django.utils.translation import get_language
from django.conf import settings


def get_localised_field_value(instance, field_name):
    try:
        current_language = get_language()
        default_language = settings.LANGUAGES[0][0]

        current_field_name = '%s_%s' % (field_name, current_language)
        default_field_name = '%s_%s' % (field_name, default_language)

        field_value = getattr(instance, current_field_name, '')

        if field_value:
            return field_value

        elif current_field_name != default_field_name:
            field_value = getattr(instance, default_field_name, '')
            return field_value

    except Exception as e:
        print(e)
        return ''
