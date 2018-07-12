from django.urls import LocalePrefixPattern, URLResolver
from django.conf import settings
from django.utils.translation import activate, get_language


class ActiveLocalePrefixPattern(LocalePrefixPattern):
    """Patched version of LocalePrefixPattern for i18n_patterns."""

    @property
    def language_prefix(self):
        """Overwrite the default language_prefix function within LocalePrefixPattern.

        This allows us to check for activated languages before resolving URL.
        """
        language_code = get_language() or settings.LANGUAGE_CODE
        active_language_codes = [active_language_code for active_language_code, _ in settings.ACTIVE_LANGUAGES]
        if language_code not in active_language_codes:
            language_code = settings.LANGUAGE_CODE
            activate(language_code)
        if language_code == settings.LANGUAGE_CODE and not self.prefix_default_language:
            return ''
        return '%s/' % language_code


def i18n_patterns(*urls, prefix_default_language=True):
    """Add the language code prefix to every URL pattern within this function.

    This may only be used in the root URLconf, not in an included URLconf.
    """
    if not settings.USE_I18N:
        return list(urls)
    return [
        URLResolver(
            ActiveLocalePrefixPattern(prefix_default_language=prefix_default_language),
            list(urls),
        )
    ]
