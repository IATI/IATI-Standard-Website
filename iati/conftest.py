import os
import pytest
from splinter import Browser
from django.core.management import call_command
from iati.settings.local import DJANGO_ADMIN_USER, DJANGO_ADMIN_PASS
from django.contrib.auth.models import User

LOCALHOST = 'http://127.0.0.1:8000/'
os.environ['LIVE_SERVER_URL'] = LOCALHOST


@pytest.fixture(scope='session', params=[
    'chrome',
    'firefox'
])
def multibrowser(request):
    """Create multiple browsers for tests."""
    return Browser(request.param)


@pytest.fixture(scope='function')
def admin_browser(browser):
    """Create a browser that is logged in to the CMS."""
    admin_page = os.environ['LIVE_SERVER_URL']+'/admin/'
    browser.visit(admin_page)
    browser.fill('username', DJANGO_ADMIN_USER)
    browser.fill('password', DJANGO_ADMIN_PASS)
    sign_in_button = browser.find_by_css("button").first
    sign_in_button.click()
    return browser


@pytest.fixture(scope='module')
def django_db_setup(django_db_setup, django_db_blocker, live_server):
    os.environ['LIVE_SERVER_URL'] = live_server.url
    with django_db_blocker.unblock():
        if not User.objects.filter(username=DJANGO_ADMIN_USER).exists():
            User.objects.create_superuser(DJANGO_ADMIN_USER, "admin@email.com", DJANGO_ADMIN_PASS)
        call_command('createdefaultpages')
    return django_db_setup
