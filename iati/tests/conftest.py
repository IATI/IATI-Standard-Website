import pytest
from splinter import Browser
from iati.settings.dev import DJANGO_ADMIN_USER, DJANGO_ADMIN_PASS

LOCALHOST = 'http://127.0.0.1:8000/'


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
    browser.visit(LOCALHOST+'admin/')
    browser.fill('username', DJANGO_ADMIN_USER)
    browser.fill('password', DJANGO_ADMIN_PASS)
    sign_in_button = browser.find_by_css("button").first
    sign_in_button.click()
    return browser
