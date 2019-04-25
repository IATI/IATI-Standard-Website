"""Settings for production environments (overrides base settings)."""

from .base import *  # noqa: F401, F403  # pylint: disable=unused-wildcard-import, wildcard-import

DEBUG = False

PATTERN_LIBRARY_URL = 'https://styles.iatistandard.org/'

try:
    from .local import *  # noqa: F401, F403  # pylint: disable=unused-wildcard-import, wildcard-import
except ImportError:
    pass
