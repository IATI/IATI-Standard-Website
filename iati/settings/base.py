"""Django settings for iati project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

# Mark language names as translation strings
from django.utils.translation import gettext_lazy as _

from django.test.utils import ignore_warnings

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

ADMINS = (
    ('Alex Miller', 'alex.miller@devinit.org'),
    ('Nik Osvalds', 'nik.osvalds@devinit.org'),
    ('Alex Lydiate', 'alexl@devinit.org'),
    ('IATI Code', 'code@iatistandard.org'),
)

SECRET_KEY = 'enter-a-long-unguessable-string-here'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'wagtail_modeltranslation',
    'wagtail_modeltranslation.makemigrations',
    'wagtail_modeltranslation.migrate',
    'home',
    'search',
    'about',
    'contact',
    'events',
    'guidance_and_support',
    'news',
    'iati_standard',
    'using_data',
    'tools',
    'dashboard',
    'navigation',
    'get_involved',
    'governance',
    'taxonomies',
    'common',
    'testimonials',
    'notices',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',
    'haystack',
    'import_export',
    'widget_tweaks',
    'snowpenguin.django.recaptcha3',
    'prettyjson',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'wagtail.contrib.search_promotions',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'wagtail.contrib.settings',
    'wagtail.contrib.modeladmin',

    'modeltranslation_sync',
    'django_extensions',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    # For determining browser locale, must come after sessions and cache (not present) and before common
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'iati.custom_middleware.RedirectIATISites',
    'iati.custom_middleware.LowercaseMiddleware',
    'opencensus.ext.django.middleware.OpencensusMiddleware',
]

ROOT_URLCONF = 'iati.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'iati.context_processors.globals',
                'iati.context_processors.captchakey',
            ],
        },
    },
]

WSGI_APPLICATION = 'iati.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASE_URL = os.getenv('DATABASE_URL', None)

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config()
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DATABASE_NAME'),
            'USER': os.getenv('DATABASE_USER'),
            'PASSWORD': os.getenv('DATABASE_PASS'),
            'HOST': os.getenv('DATABASE_HOST'),
            'PORT': os.getenv('DATABASE_PORT'),
            'CONN_MAX_AGE': 60,
            'OPTIONS': {'sslmode': 'require'},
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
    ('es', _('Spanish')),
    ('pt', _('Portuguese')),
]

ACTIVE_LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'patterns/converted-html/assets'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/assets/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

REFERENCE_DOWNLOAD_ROOT = os.path.join(BASE_DIR, 'reference_downloads')
REFERENCE_DOWNLOAD_URL = '/reference_downloads/'

DOCUMENTS_SLUG = 'documents'
DOCUMENTS_URL = '/{}/'.format(DOCUMENTS_SLUG)

ADMIN_SLUG = 'cms'
ADMIN_URL = '/{}/'.format(ADMIN_SLUG)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Wagtail settings
WAGTAIL_SITE_NAME = "iati"
WAGTAIL_FRONTEND_LOGIN_TEMPLATE = 'wagtailadmin/login.html'

# Reference namespaces for URL redirection
# `EXACT` catches wildcards, redirects to single page
# `WILDCARD` catches wildcards, redirects old path to new path
REFERENCE_NAMESPACE_EXACT_REDIRECT_DICT = {
    "archived/101": "/en/iati-standard/101",
    "archived/102": "/en/iati-standard/102",
    "archived/103": "/en/iati-standard/103",
    "developer": "/en/guidance/developer/",
    "203/developer": "/en/guidance/developer/",
    "202/developer": "/en/guidance/developer/",
    "201/developer": "/en/guidance/developer/",
    "105/developer": "/en/guidance/developer/",
    "104/developer": "/en/guidance/developer/",
    "introduction": "/en/iati-standard/",
    "guidance/datastore": "/en/iati-tools-and-resources/iati-datastore/",
    "203/upgrades/all-versions": "/en/iati-standard/upgrades/how-we-manage-the-standard/versions/",
    "203/upgrades/all-versions/previous-process": "/en/iati-standard/upgrades/how-we-manage-the-standard/previous-process/",
    "203/upgrades/noncore-codelist-changelog": "/en/iati-standard/upgrades/upgrade-changelogs/noncore-codelist-changelog/",
    "203/upgrades/decimal-upgrade-to-2-03": "/en/iati-standard/upgrades/upgrade-changelogs/decimal-upgrade-to-2-03/",
    "203/upgrades/decimal-upgrade-to-2-02": "/en/iati-standard/upgrades/upgrade-changelogs/decimal-upgrade-to-2-02/",
    "203/upgrades/integer-upgrade-to-2-01": "/en/iati-standard/upgrades/upgrade-changelogs/integer-upgrade-to-2-01/",
    "203/upgrades/decimal-upgrade-to-1-05": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-05/",
    "203/upgrades/decimal-upgrade-to-1-04": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-04/",
    "203/upgrades/decimal-upgrade-to-1-03": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-03/",
    "203/upgrades/decimal-upgrade-to-1-02": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-02/",
    "203/upgrades": "/en/iati-standard/upgrades/",
    "203/codelists-guides/codelist-management": "/en/iati-standard/upgrades/how-we-manage-the-standard/codelist-management/",
    "202/upgrades/all-versions": "/en/iati-standard/upgrades/how-we-manage-the-standard/versions/",
    "202/upgrades/all-versions/previous-process": "/en/iati-standard/upgrades/how-we-manage-the-standard/previous-process/",
    "202/upgrades/noncore-codelist-changelog": "/en/iati-standard/upgrades/upgrade-changelogs/noncore-codelist-changelog/",
    "202/upgrades/decimal-upgrade-to-2-03": "/en/iati-standard/upgrades/upgrade-changelogs/decimal-upgrade-to-2-03/",
    "202/upgrades/decimal-upgrade-to-2-02": "/en/iati-standard/upgrades/upgrade-changelogs/decimal-upgrade-to-2-02/",
    "202/upgrades/integer-upgrade-to-2-01": "/en/iati-standard/upgrades/upgrade-changelogs/integer-upgrade-to-2-01/",
    "202/upgrades/decimal-upgrade-to-1-05": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-05/",
    "202/upgrades/decimal-upgrade-to-1-04": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-04/",
    "202/upgrades/decimal-upgrade-to-1-03": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-03/",
    "202/upgrades/decimal-upgrade-to-1-02": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-02/",
    "202/upgrades": "/en/iati-standard/upgrades/",
    "202/codelists-guides/codelist-management": "/en/iati-standard/upgrades/how-we-manage-the-standard/codelist-management/",
    "201/upgrades/all-versions": "/en/iati-standard/upgrades/how-we-manage-the-standard/versions/",
    "201/upgrades/all-versions/previous-process": "/en/iati-standard/upgrades/how-we-manage-the-standard/previous-process/",
    "201/upgrades/noncore-codelist-changelog": "/en/iati-standard/upgrades/upgrade-changelogs/noncore-codelist-changelog/",
    "201/upgrades/decimal-upgrade-to-2-03": "/en/iati-standard/upgrades/upgrade-changelogs/decimal-upgrade-to-2-03/",
    "201/upgrades/decimal-upgrade-to-2-02": "/en/iati-standard/upgrades/upgrade-changelogs/decimal-upgrade-to-2-02/",
    "201/upgrades/integer-upgrade-to-2-01": "/en/iati-standard/upgrades/upgrade-changelogs/integer-upgrade-to-2-01/",
    "201/upgrades/decimal-upgrade-to-1-05": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-05/",
    "201/upgrades/decimal-upgrade-to-1-04": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-04/",
    "201/upgrades/decimal-upgrade-to-1-03": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-03/",
    "201/upgrades/decimal-upgrade-to-1-02": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-02/",
    "201/upgrades": "/en/iati-standard/upgrades/",
    "201/codelists-guides/codelist-management": "/en/iati-standard/upgrades/how-we-manage-the-standard/codelist-management/",
    "105/upgrades/all-versions": "/en/iati-standard/upgrades/how-we-manage-the-standard/versions/",
    "105/upgrades/all-versions/previous-process": "/en/iati-standard/upgrades/how-we-manage-the-standard/previous-process/",
    "105/upgrades/noncore-codelist-changelog": "/en/iati-standard/upgrades/upgrade-changelogs/noncore-codelist-changelog/",
    "105/upgrades/decimal-upgrade-to-2-03": "/en/iati-standard/upgrades/upgrade-changelogs/decimal-upgrade-to-2-03/",
    "105/upgrades/decimal-upgrade-to-2-02": "/en/iati-standard/upgrades/upgrade-changelogs/decimal-upgrade-to-2-02/",
    "105/upgrades/integer-upgrade-to-2-01": "/en/iati-standard/upgrades/upgrade-changelogs/integer-upgrade-to-2-01/",
    "105/upgrades/decimal-upgrade-to-1-05": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-05/",
    "105/upgrades/decimal-upgrade-to-1-04": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-04/",
    "105/upgrades/decimal-upgrade-to-1-03": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-03/",
    "105/upgrades/decimal-upgrade-to-1-02": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-02/",
    "105/upgrades": "/en/iati-standard/upgrades/",
    "105/codelists-guides/codelist-management": "/en/iati-standard/upgrades/how-we-manage-the-standard/codelist-management/",
    "104/upgrades/all-versions": "/en/iati-standard/upgrades/how-we-manage-the-standard/versions/",
    "104/upgrades/all-versions/previous-process": "/en/iati-standard/upgrades/how-we-manage-the-standard/previous-process/",
    "104/upgrades/noncore-codelist-changelog": "/en/iati-standard/upgrades/upgrade-changelogs/noncore-codelist-changelog/",
    "104/upgrades/decimal-upgrade-to-2-03": "/en/iati-standard/upgrades/upgrade-changelogs/decimal-upgrade-to-2-03/",
    "104/upgrades/decimal-upgrade-to-2-02": "/en/iati-standard/upgrades/upgrade-changelogs/decimal-upgrade-to-2-02/",
    "104/upgrades/integer-upgrade-to-2-01": "/en/iati-standard/upgrades/upgrade-changelogs/integer-upgrade-to-2-01/",
    "104/upgrades/decimal-upgrade-to-1-05": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-05/",
    "104/upgrades/decimal-upgrade-to-1-04": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-04/",
    "104/upgrades/decimal-upgrade-to-1-03": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-03/",
    "104/upgrades/decimal-upgrade-to-1-02": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-02/",
    "104/upgrades": "/en/iati-standard/upgrades/",
    "104/codelists-guides/codelist-management": "/en/iati-standard/upgrades/how-we-manage-the-standard/codelist-management/",
    "upgrades/all-versions": "/en/iati-standard/upgrades/how-we-manage-the-standard/versions/",
    "upgrades/all-versions/previous-process": "/en/iati-standard/upgrades/how-we-manage-the-standard/previous-process/",
    "upgrades/noncore-codelist-changelog": "/en/iati-standard/upgrades/upgrade-changelogs/noncore-codelist-changelog/",
    "upgrades/decimal-upgrade-to-2-03": "/en/iati-standard/upgrades/upgrade-changelogs/decimal-upgrade-to-2-03/",
    "upgrades/decimal-upgrade-to-2-02": "/en/iati-standard/upgrades/upgrade-changelogs/decimal-upgrade-to-2-02/",
    "upgrades/integer-upgrade-to-2-01": "/en/iati-standard/upgrades/upgrade-changelogs/integer-upgrade-to-2-01/",
    "upgrades/decimal-upgrade-to-1-05": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-05/",
    "upgrades/decimal-upgrade-to-1-04": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-04/",
    "upgrades/decimal-upgrade-to-1-03": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-03/",
    "upgrades/decimal-upgrade-to-1-02": "/en/iati-standard/upgrades/upgrade-changelogs/v1-upgrades/decimal-upgrade-to-1-02/",
    "upgrades": "/en/iati-standard/upgrades/",
    "codelists-guides/codelist-management": "/en/iati-standard/upgrades/how-we-manage-the-standard/codelist-management/",
    "203/codelists-guides/codelist-api": "/en/guidance/developer/codelist-api/",
    "203/activity-standard/elements": "/en/iati-standard/203/activity-standard/iati-activities/",
    "203/organisation-standard/elements": "/en/iati-standard/203/organisation-standard/iati-organisations/",
    "203/organisation-identifiers": "/en/guidance/preparing-organisation/organisation-account/how-to-create-your-iati-organisation-identifier/",
    "202/codelists-guides/codelist-api": "/en/guidance/developer/codelist-api/",
    "202/activity-standard/elements": "/en/iati-standard/202/activity-standard/iati-activities/",
    "202/organisation-standard/elements": "/en/iati-standard/202/organisation-standard/iati-organisations/",
    "202/organisation-identifiers": "/en/guidance/preparing-organisation/organisation-account/how-to-create-your-iati-organisation-identifier/",
    "201/codelists-guides/codelist-api": "/en/guidance/developer/codelist-api/",
    "201/activity-standard/elements": "/en/iati-standard/201/activity-standard/iati-activities/",
    "201/organisation-standard/elements": "/en/iati-standard/201/organisation-standard/iati-organisations/",
    "201/organisation-identifiers": "/en/guidance/preparing-organisation/organisation-account/how-to-create-your-iati-organisation-identifier/",
    "203/activity-standard/overview/activity-file": "/en/guidance/preparing-data/activity-information/",
    "203/activity-standard/overview/iati-activity": "/en/guidance/preparing-data/activity-information/",
    "203/activity-standard/overview/iati-identifier": "/en/guidance/preparing-data/activity-information/creating-iati-identifiers/",
    "203/activity-standard/overview/dates": "/en/guidance/standard-guidance/activity-dates-status/",
    "203/activity-standard/overview/organisations": "/en/guidance/standard-guidance/activity-participants/",
    "203/activity-standard/overview/geography": "/en/guidance/standard-guidance/countries-regions/",
    "203/activity-standard/overview/country-budget-alignment": "/en/guidance/standard-guidance/country-budget-alignment/",
    "203/activity-standard/overview/classifications": "/en/guidance/standard-guidance/activity-classifications/",
    "203/activity-standard/overview/budgets": "/en/guidance/standard-guidance/activity-budgets/",
    "203/activity-standard/overview/transactions": "/en/guidance/standard-guidance/financial-transactions/",
    "203/activity-standard/overview/result": "/en/guidance/standard-guidance/results/",
    "203/activity-standard/overview/related-data": "/en/guidance/standard-guidance/related-data/",
    "203/activity-standard/overview/linked-documents": "/en/guidance/standard-guidance/related-documents/",
    "203/activity-standard/overview/crs-fss": "/en/guidance/standard-guidance/crs-fss/",
    "203/activity-standard/overview/conditions": "/en/guidance/standard-guidance/conditions/",
    "203/activity-standard/overview/contact-info": "/en/guidance/standard-guidance/",
    "203/activity-standard/overview/humanitarian-reporting": "/en/guidance/standard-guidance/humanitarian/",
    "203/activity-standard/overview/self-defined-vocabularies": "/en/guidance/standard-guidance/self-defined-vocabularies/",
    "203/activity-standard/overview/sustainable-development-goals": "/en/guidance/standard-guidance/sdg-guidance/",
    "203/activity-standard/overview": "/en/guidance/standard-guidance/",
    "203/organisation-standard/overview/organisation-file": "/en/guidance/preparing-data/activity-information/",
    "203/organisation-standard/overview/iati-organisation": "/en/guidance/preparing-data/organisation-infromation/",
    "203/organisation-standard/overview/organisations": "/en/guidance/standard-guidance/activity-participants/",
    "203/organisation-standard/overview/budgets": "/en/guidance/standard-guidance/organisation-budgets-spend/",
    "203/organisation-standard/overview/documents": "/en/guidance/standard-guidance/related-documents/",
    "203/organisation-standard/overview": "/en/guidance/standard-guidance/",
    "202/activity-standard/overview/activity-file": "/en/guidance/preparing-data/activity-information/",
    "202/activity-standard/overview/iati-activity": "/en/guidance/preparing-data/activity-information/",
    "202/activity-standard/overview/iati-identifier": "/en/guidance/preparing-data/activity-information/creating-iati-identifiers/",
    "202/activity-standard/overview/dates": "/en/guidance/standard-guidance/activity-dates-status/",
    "202/activity-standard/overview/organisations": "/en/guidance/standard-guidance/activity-participants/",
    "202/activity-standard/overview/geography": "/en/guidance/standard-guidance/countries-regions/",
    "202/activity-standard/overview/country-budget-alignment": "/en/guidance/standard-guidance/country-budget-alignment/",
    "202/activity-standard/overview/classifications": "/en/guidance/standard-guidance/activity-classifications/",
    "202/activity-standard/overview/budgets": "/en/guidance/standard-guidance/activity-budgets/",
    "202/activity-standard/overview/transactions": "/en/guidance/standard-guidance/financial-transactions/",
    "202/activity-standard/overview/result": "/en/guidance/standard-guidance/results/",
    "202/activity-standard/overview/related-data": "/en/guidance/standard-guidance/related-data/",
    "202/activity-standard/overview/linked-documents": "/en/guidance/standard-guidance/related-documents/",
    "202/activity-standard/overview/crs-fss": "/en/guidance/standard-guidance/crs-fss/",
    "202/activity-standard/overview/conditions": "/en/guidance/standard-guidance/conditions/",
    "202/activity-standard/overview/contact-info": "/en/guidance/standard-guidance/",
    "202/activity-standard/overview/humanitarian-reporting": "/en/guidance/standard-guidance/humanitarian/",
    "202/activity-standard/overview/self-defined-vocabularies": "/en/guidance/standard-guidance/self-defined-vocabularies/",
    "202/activity-standard/overview/sustainable-development-goals": "/en/guidance/standard-guidance/sdg-guidance/",
    "202/activity-standard/overview": "/en/guidance/standard-guidance/",
    "202/organisation-standard/overview/organisation-file": "/en/guidance/preparing-data/activity-information/",
    "202/organisation-standard/overview/iati-organisation": "/en/guidance/preparing-data/organisation-infromation/",
    "202/organisation-standard/overview/organisations": "/en/guidance/standard-guidance/activity-participants/",
    "202/organisation-standard/overview/budgets": "/en/guidance/standard-guidance/organisation-budgets-spend/",
    "202/organisation-standard/overview/documents": "/en/guidance/standard-guidance/related-documents/",
    "202/organisation-standard/overview": "/en/guidance/standard-guidance/",
    "201/activity-standard/overview/activity-file": "/en/guidance/preparing-data/activity-information/",
    "201/activity-standard/overview/iati-activity": "/en/guidance/preparing-data/activity-information/",
    "201/activity-standard/overview/iati-identifier": "/en/guidance/preparing-data/activity-information/creating-iati-identifiers/",
    "201/activity-standard/overview/dates": "/en/guidance/standard-guidance/activity-dates-status/",
    "201/activity-standard/overview/organisations": "/en/guidance/standard-guidance/activity-participants/",
    "201/activity-standard/overview/geography": "/en/guidance/standard-guidance/countries-regions/",
    "201/activity-standard/overview/country-budget-alignment": "/en/guidance/standard-guidance/country-budget-alignment/",
    "201/activity-standard/overview/classifications": "/en/guidance/standard-guidance/activity-classifications/",
    "201/activity-standard/overview/budgets": "/en/guidance/standard-guidance/activity-budgets/",
    "201/activity-standard/overview/transactions": "/en/guidance/standard-guidance/financial-transactions/",
    "201/activity-standard/overview/result": "/en/guidance/standard-guidance/results/",
    "201/activity-standard/overview/related-data": "/en/guidance/standard-guidance/related-data/",
    "201/activity-standard/overview/linked-documents": "/en/guidance/standard-guidance/related-documents/",
    "201/activity-standard/overview/crs-fss": "/en/guidance/standard-guidance/crs-fss/",
    "201/activity-standard/overview/conditions": "/en/guidance/standard-guidance/conditions/",
    "201/activity-standard/overview/contact-info": "/en/guidance/standard-guidance/",
    "201/activity-standard/overview/humanitarian-reporting": "/en/guidance/standard-guidance/humanitarian/",
    "201/activity-standard/overview/self-defined-vocabularies": "/en/guidance/standard-guidance/self-defined-vocabularies/",
    "201/activity-standard/overview/sustainable-development-goals": "/en/guidance/standard-guidance/sdg-guidance/",
    "201/activity-standard/overview": "/en/guidance/standard-guidance/",
    "201/organisation-standard/overview/organisation-file": "/en/guidance/preparing-data/activity-information/",
    "201/organisation-standard/overview/iati-organisation": "/en/guidance/preparing-data/organisation-infromation/",
    "201/organisation-standard/overview/organisations": "/en/guidance/standard-guidance/activity-participants/",
    "201/organisation-standard/overview/budgets": "/en/guidance/standard-guidance/organisation-budgets-spend/",
    "201/organisation-standard/overview/documents": "/en/guidance/standard-guidance/related-documents/",
    "201/organisation-standard/overview": "/en/guidance/standard-guidance/",
    "105/activity-standard/overview/activity-file": "/en/guidance/preparing-data/activity-information/",
    "105/activity-standard/overview/iati-activity": "/en/guidance/preparing-data/activity-information/",
    "105/activity-standard/overview/iati-identifier": "/en/guidance/preparing-data/activity-information/creating-iati-identifiers/",
    "105/activity-standard/overview/dates": "/en/guidance/standard-guidance/activity-dates-status/",
    "105/activity-standard/overview/organisations": "/en/guidance/standard-guidance/activity-participants/",
    "105/activity-standard/overview/geography": "/en/guidance/standard-guidance/countries-regions/",
    "105/activity-standard/overview/country-budget-alignment": "/en/guidance/standard-guidance/country-budget-alignment/",
    "105/activity-standard/overview/classifications": "/en/guidance/standard-guidance/activity-classifications/",
    "105/activity-standard/overview/budgets": "/en/guidance/standard-guidance/activity-budgets/",
    "105/activity-standard/overview/transactions": "/en/guidance/standard-guidance/financial-transactions/",
    "105/activity-standard/overview/result": "/en/guidance/standard-guidance/results/",
    "105/activity-standard/overview/related-data": "/en/guidance/standard-guidance/related-data/",
    "105/activity-standard/overview/linked-documents": "/en/guidance/standard-guidance/related-documents/",
    "105/activity-standard/overview/crs-fss": "/en/guidance/standard-guidance/crs-fss/",
    "105/activity-standard/overview/conditions": "/en/guidance/standard-guidance/conditions/",
    "105/activity-standard/overview/contact-info": "/en/guidance/standard-guidance/",
    "105/activity-standard/overview/humanitarian-reporting": "/en/guidance/standard-guidance/humanitarian/",
    "105/activity-standard/overview/self-defined-vocabularies": "/en/guidance/standard-guidance/self-defined-vocabularies/",
    "105/activity-standard/overview/sustainable-development-goals": "/en/guidance/standard-guidance/sdg-guidance/",
    "105/activity-standard/overview": "/en/guidance/standard-guidance/",
    "105/organisation-standard/overview/organisation-file": "/en/guidance/preparing-data/activity-information/",
    "105/organisation-standard/overview/iati-organisation": "/en/guidance/preparing-data/organisation-infromation/",
    "105/organisation-standard/overview/organisations": "/en/guidance/standard-guidance/activity-participants/",
    "105/organisation-standard/overview/budgets": "/en/guidance/standard-guidance/organisation-budgets-spend/",
    "105/organisation-standard/overview/documents": "/en/guidance/standard-guidance/related-documents/",
    "105/organisation-standard/overview": "/en/guidance/standard-guidance/",
    "104/activity-standard/overview/activity-file": "/en/guidance/preparing-data/activity-information/",
    "104/activity-standard/overview/iati-activity": "/en/guidance/preparing-data/activity-information/",
    "104/activity-standard/overview/iati-identifier": "/en/guidance/preparing-data/activity-information/creating-iati-identifiers/",
    "104/activity-standard/overview/dates": "/en/guidance/standard-guidance/activity-dates-status/",
    "104/activity-standard/overview/organisations": "/en/guidance/standard-guidance/activity-participants/",
    "104/activity-standard/overview/geography": "/en/guidance/standard-guidance/countries-regions/",
    "104/activity-standard/overview/country-budget-alignment": "/en/guidance/standard-guidance/country-budget-alignment/",
    "104/activity-standard/overview/classifications": "/en/guidance/standard-guidance/activity-classifications/",
    "104/activity-standard/overview/budgets": "/en/guidance/standard-guidance/activity-budgets/",
    "104/activity-standard/overview/transactions": "/en/guidance/standard-guidance/financial-transactions/",
    "104/activity-standard/overview/result": "/en/guidance/standard-guidance/results/",
    "104/activity-standard/overview/related-data": "/en/guidance/standard-guidance/related-data/",
    "104/activity-standard/overview/linked-documents": "/en/guidance/standard-guidance/related-documents/",
    "104/activity-standard/overview/crs-fss": "/en/guidance/standard-guidance/crs-fss/",
    "104/activity-standard/overview/conditions": "/en/guidance/standard-guidance/conditions/",
    "104/activity-standard/overview/contact-info": "/en/guidance/standard-guidance/",
    "104/activity-standard/overview/humanitarian-reporting": "/en/guidance/standard-guidance/humanitarian/",
    "104/activity-standard/overview/self-defined-vocabularies": "/en/guidance/standard-guidance/self-defined-vocabularies/",
    "104/activity-standard/overview/sustainable-development-goals": "/en/guidance/standard-guidance/sdg-guidance/",
    "104/activity-standard/overview": "/en/guidance/standard-guidance/",
    "104/organisation-standard/overview/organisation-file": "/en/guidance/preparing-data/activity-information/",
    "104/organisation-standard/overview/iati-organisation": "/en/guidance/preparing-data/organisation-infromation/",
    "104/organisation-standard/overview/organisations": "/en/guidance/standard-guidance/activity-participants/",
    "104/organisation-standard/overview/budgets": "/en/guidance/standard-guidance/organisation-budgets-spend/",
    "104/organisation-standard/overview/documents": "/en/guidance/standard-guidance/related-documents/",
    "104/organisation-standard/overview": "/en/guidance/standard-guidance/",
    "activity-standard/overview/activity-file": "/en/guidance/preparing-data/activity-information/",
    "activity-standard/overview/iati-activity": "/en/guidance/preparing-data/activity-information/",
    "activity-standard/overview/iati-identifier": "/en/guidance/preparing-data/activity-information/creating-iati-identifiers/",
    "activity-standard/overview/dates": "/en/guidance/standard-guidance/activity-dates-status/",
    "activity-standard/overview/organisations": "/en/guidance/standard-guidance/activity-participants/",
    "activity-standard/overview/geography": "/en/guidance/standard-guidance/countries-regions/",
    "activity-standard/overview/country-budget-alignment": "/en/guidance/standard-guidance/country-budget-alignment/",
    "activity-standard/overview/classifications": "/en/guidance/standard-guidance/activity-classifications/",
    "activity-standard/overview/budgets": "/en/guidance/standard-guidance/activity-budgets/",
    "activity-standard/overview/transactions": "/en/guidance/standard-guidance/financial-transactions/",
    "activity-standard/overview/result": "/en/guidance/standard-guidance/results/",
    "activity-standard/overview/related-data": "/en/guidance/standard-guidance/related-data/",
    "activity-standard/overview/linked-documents": "/en/guidance/standard-guidance/related-documents/",
    "activity-standard/overview/crs-fss": "/en/guidance/standard-guidance/crs-fss/",
    "activity-standard/overview/conditions": "/en/guidance/standard-guidance/conditions/",
    "activity-standard/overview/contact-info": "/en/guidance/standard-guidance/",
    "activity-standard/overview/humanitarian-reporting": "/en/guidance/standard-guidance/humanitarian/",
    "activity-standard/overview/self-defined-vocabularies": "/en/guidance/standard-guidance/self-defined-vocabularies/",
    "activity-standard/overview/sustainable-development-goals": "/en/guidance/standard-guidance/sdg-guidance/",
    "activity-standard/overview": "/en/guidance/standard-guidance/",
    "organisation-standard/overview/organisation-file": "/en/guidance/preparing-data/activity-information/",
    "organisation-standard/overview/iati-organisation": "/en/guidance/preparing-data/organisation-infromation/",
    "organisation-standard/overview/organisations": "/en/guidance/standard-guidance/activity-participants/",
    "organisation-standard/overview/budgets": "/en/guidance/standard-guidance/organisation-budgets-spend/",
    "organisation-standard/overview/documents": "/en/guidance/standard-guidance/related-documents/",
    "organisation-standard/overview": "/en/guidance/standard-guidance/",
}
REFERENCE_NAMESPACE_WILDCARD_REDIRECT_DICT = {
    "203/codelists/downloads": "/reference_downloads/",
    "203/schema/downloads": "/reference_downloads/",
    "202/codelists/downloads": "/reference_downloads/",
    "202/schema/downloads": "/reference_downloads/",
    "201/codelists/downloads": "/reference_downloads/",
    "201/schema/downloads": "/reference_downloads/",
    "105/codelists/downloads": "/reference_downloads/",
    "105/schema/downloads": "/reference_downloads/",
    "104/codelists/downloads": "/reference_downloads/",
    "104/schema/downloads": "/reference_downloads/",
    "downloads": "/reference_downloads/archive/",
    "101": "/en/iati-standard/",
    "102": "/en/iati-standard/",
    "103": "/en/iati-standard/",
    "104": "/en/iati-standard/",
    "105": "/en/iati-standard/",
    "201": "/en/iati-standard/",
    "202": "/en/iati-standard/",
    "203": "/en/iati-standard/",
    "activity-standard": "/en/iati-standard/203/",
    "codelists/downloads": "/reference_downloads/203/",
    "codelists": "/en/iati-standard/203/",
    "namespaces-extensions": "/en/iati-standard/203/",
    "organisation-standard": "/en/iati-standard/203/",
    "reference": "/en/iati-standard/203/",
    "rulesets": "/en/iati-standard/203/",
    "schema/downloads": "/reference_downloads/203/",
    "schema": "/en/iati-standard/203/",
}

EXACT_REFERENCE_NAMESPACES = list(REFERENCE_NAMESPACE_EXACT_REDIRECT_DICT.keys())
WILDCARD_REFERENCE_NAMESPACES = list(REFERENCE_NAMESPACE_WILDCARD_REDIRECT_DICT.keys())

REFERENCE_REDIRECT_BASE_URL = 'https://iatistandard.org'

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://iatistandard.org'

# Modeltranslation sync Settings
MODELTRANSLATION_LOCALE_PATH = os.path.join(BASE_DIR, 'locale')
LOCALE_PATHS = (MODELTRANSLATION_LOCALE_PATH,)
MODELTRANSLATION_PO_FILE = "iati.po"

# Community URL
COMMUNITY_URL = 'https://discuss.iatistandard.org/'

# Social Media
TWITTER_HANDLE = 'IATI_aid'
YOUTUBE_CHANNEL_URL = 'https://www.youtube.com/channel/UCAVH1gcgJXElsj8ENC-bDQQ'

# Relative URL for the default social media sharing image
DEFAULT_SHARE_IMAGE_URL = 'img/iati-share-social.png'


# Search settings
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.elasticsearch6',
        'URLS': [os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')],
        'INDEX': 'iati',
    },
}
HAYSTACK_CONNECTIONS = {
    'default': {},
}
HAYSTACK_CUSTOM_HIGHLIGHTER = 'search.utils.CustomHighlighter'

# Zendesk and recaptcha settings
ZENDESK_REQUEST_URL = 'https://iati.zendesk.com/api/v2/requests.json'
ZENDESK_CAPTCHA_FIELD_ID = os.getenv('ZENDESK_CAPTCHA_FIELD_ID')
ZENDESK_SUSPICIOUS_FIELD_ID = os.getenv('ZENDESK_SUSPICIOUS_FIELD_ID')
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_DEFAULT_ACTION = 'contact'
RECAPTCHA_SCORE_THRESHOLD = float(os.getenv('RECAPTCHA_SCORE_THRESHOLD', 0.5))

# Github settings

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Blob storage
AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')

if AZURE_ACCOUNT_NAME:
    REFERENCE_DOWNLOAD_ROOT = os.path.join('/reference_downloads')
    AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')
    AZURE_CONTAINER = os.getenv('AZURE_CONTAINER')
    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
    STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'

# App insights

APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')

if APPLICATIONINSIGHTS_CONNECTION_STRING:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(levelname)s - %(processName)s - %(name)s\n%(message)s",
            },
        },
        "handlers": {
            "azure": {
                "class": "opencensus.ext.azure.log_exporter.AzureLogHandler",
                "formatter": "default",
                "connection_string": APPLICATIONINSIGHTS_CONNECTION_STRING,
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        'loggers': {
            'django': {
                'handlers': ["azure", "console"],
                'level': "ERROR",
                'propagate': True,
            },
        },
    }

# Ignore Whitenoise error when running with Azure storage
ignore_warnings(message="No directory at", module="whitenoise.base").enable()

# Configure PK field for non-Page models for Django 3.2+
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Default responsive image file format
WAGTAILIMAGES_FORMAT_CONVERSIONS = {
    'webp': 'webp',
    'jpg': 'webp',
    'jpeg': 'webp',
    'png': 'webp',
    'bmp': 'webp',
    'gif': 'gif'
}

# Caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'wagtail_cache',
    }
}
