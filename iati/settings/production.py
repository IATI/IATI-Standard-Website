"""Settings for production environments (overrides base settings)."""

import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *  # noqa: F401, F403 # pylint: disable=unused-wildcard-import, wildcard-import

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# Overwrite this variable in local.py with another unguessable string.
SECRET_KEY = os.environ.get('SECRET_KEY')

MEDIA_ROOT = os.path.join('/', 'storage')
REFERENCE_DOWNLOAD_ROOT = os.path.join(MEDIA_ROOT, "reference_downloads")

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = [
    '0.0.0.0',
    'iatistandard.org',
    '.iatistandard.org',
]

SENTRY_DSN = os.environ.get('SENTRY_DSN', None)

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()]
    )

try:
    from .local import *  # # noqa: F401, F403  # pylint: disable=unused-wildcard-import, wildcard-import
except ImportError:
    pass
