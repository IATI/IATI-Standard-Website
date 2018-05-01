import pytest


def test_multiple_browsers(browser):
    """A test to test you can test with multiple browsers at once."""
    browser.visit('https://www.google.com')
    assert browser.url == 'https://www.google.com/'
    browser.quit()

# def test_default_pages_exist(available_browser)
