"""Settings for production environments (overrides base settings)."""

from .base import *  # noqa: F401, F403  # pylint: disable=unused-wildcard-import, wildcard-import

DEBUG = False

try:
    from .local import *  # noqa: F401, F403  # pylint: disable=unused-wildcard-import, wildcard-import
except ImportError:
    pass
