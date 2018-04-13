"""Settings for production environments (overrides base settings)."""

from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass
