"""Settings for dev environments (overrides base settings)."""
import os
from .base import *  # noqa: F401, F403 # pylint: disable=unused-wildcard-import, wildcard-import

ALLOWED_HOSTS = ['*']

SECRET_KEY = '-sg0o=f6(j3!4u6^86!j@0&l^3clslh-#f@02d2^p_4vy0ma0y'

if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travisci',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

USE_TZ = False

MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media') # noqa

try:
    from .local import *  # # noqa: F401, F403  # pylint: disable=unused-wildcard-import, wildcard-import
except ImportError:
    pass
