import pytest
from splinter import Browser


@pytest.fixture(scope='session', params=[
    'chrome',
    'firefox'
])
def browser(request):
    """Override splinter webdriver."""
    return Browser(request.param)
