from django.urls import LocalePrefixPattern
from django.conf import settings
from django.utils.translation import activate, get_language


@property
def language_prefix(self):
    """
    Overwrite the default language_prefix function within LocalePrefixPattern.
    This allows us to check for activated languages before resolving URL.
    """
    language_code = get_language() or settings.LANGUAGE_CODE
    if language_code not in [active_language_code for active_language_code, active_language_name in settings.ACTIVE_LANGUAGES]:
        language_code = settings.LANGUAGE_CODE
        activate(language_code)
    if language_code == settings.LANGUAGE_CODE and not self.prefix_default_language:
        return ''
    return '%s/' % language_code


del LocalePrefixPattern.language_prefix
LocalePrefixPattern.language_prefix = language_prefix
