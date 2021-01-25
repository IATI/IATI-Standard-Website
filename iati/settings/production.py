"""Settings for production environments (overrides base settings)."""

import os
import sys
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *  # noqa: F401, F403 # pylint: disable=unused-wildcard-import, wildcard-import

DEBUG = False

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

APPLICATIONINSIGHTS_CONNECTION_STRING = os.environ.get('APPLICATIONINSIGHTS_CONNECTION_STRING', None)

if APPLICATIONINSIGHTS_CONNECTION_STRING:
    LOGGING = {
        "handlers": {
            "azure": {
                "level": "DEBUG",
                "class": "opencensus.ext.azure.log_exporter.AzureLogHandler",
                "instrumentation_key": APPLICATIONINSIGHTS_CONNECTION_STRING,
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "logger_name": {"handlers": ["azure", "console"]},
        },
    }

AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME', None)

if AZURE_ACCOUNT_NAME:
    AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY', None)
    AZURE_CONTAINER = os.environ.get('AZURE_CONTAINER', None)
    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
    STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'

try:
    from .local import *  # # noqa: F401, F403  # pylint: disable=unused-wildcard-import, wildcard-import
except ImportError:
    pass
