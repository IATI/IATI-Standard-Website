"""Settings for production environments (overrides base settings)."""

import os
from .base import *  # noqa: F401, F403 # pylint: disable=unused-wildcard-import, wildcard-import

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
# Overwrite this variable in local.py with another unguessable string.
SECRET_KEY = os.environ.get('SECRET_KEY')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = [
    '0.0.0.0',
    'iatistandard.org',
    '.iatistandard.org',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')

if AZURE_ACCOUNT_NAME:
    AZURE_CUSTOM_DOMAIN = 'prod-iati-website.azureedge.net'

try:
    from .local import *  # # noqa: F401, F403  # pylint: disable=unused-wildcard-import, wildcard-import
except ImportError:
    pass
