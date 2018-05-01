import pytest
from splinter import Browser


@pytest.fixture(params=[
    'chrome',
    'firefox'
])
def available_browser(request):
    """Provide available loaded browsers."""
    return Browser(request.param)


def test_multiple_browsers(available_browser):
    """A test to test you can test with multiple browsers at once."""
    available_browser.visit('https://www.google.com')
    assert available_browser.url == 'https://www.google.com/'
    available_browser.quit()
