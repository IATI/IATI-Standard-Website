"""Settings for dev environments (overrides base settings)."""
import os
from .base import *  # noqa: F401, F403 # pylint: disable=unused-wildcard-import, wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# Overwrite this variable in local.py with another unguessable string.
SECRET_KEY = os.environ.get('SECRET_KEY')

INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]


if os.environ.get('DEBUG_SERVER'):
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[: ip.rfind(".")] + ".1" for ip in ips]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = INSTALLED_APPS + [  # noqa: F405
    'debug_toolbar',
]

MIDDLEWARE = MIDDLEWARE + [  # noqa: F405
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# RESULTS_CACHE_SIZE = 100

RENDER_PANELS = False

try:
    from .local import *  # # noqa: F401, F403  # pylint: disable=unused-wildcard-import, wildcard-import
except ImportError:
    pass
