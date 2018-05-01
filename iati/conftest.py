import pytest
from splinter import Browser


@pytest.fixture(scope='session', params=[
    'chrome',
    'firefox'
])
def multibrowser(request):
    """Override splinter webdriver."""
    return Browser(request.param)
