from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-sg0o=f6(j3!4u6^86!j@0&l^3clslh-#f@02d2^p_4vy0ma0y'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['159.65.23.4']

try:
    from .local import *
except ImportError:
    pass
