"""A module of functional tests for base site functionality."""
import pytest
from conftest import LOCALHOST


DEFAULT_PAGE_NAMES = [
    'about',
    'contact',
    'events',
    'news',
    'guidance_and_support'
]


def test_google(browser):
    browser.visit("http://google.com")
    assert False

@pytest.mark.parametrize("page_name", DEFAULT_PAGE_NAMES)
def test_default_pages_exist(browser, page_name):
    """Check default pages exist."""
    browser.visit(LOCALHOST + '{}'.format(page_name))
    page_title = page_name.replace('_', ' ').capitalize()
    assert browser.title == page_title
