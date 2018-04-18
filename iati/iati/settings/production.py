"""Settings for production environments (overrides base settings)."""

from .base import *  # pylint: disable=unused-wildcard-import, wildcard-import

DEBUG = False

try:
    from .local import *  # pylint: disable=unused-wildcard-import, wildcard-import
except ImportError:
    pass
