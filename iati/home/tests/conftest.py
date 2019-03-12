import pytest
from django.test.utils import override_settings


@pytest.fixture(scope='session', autouse=True)
def custom_settings(tmpdir_factory):
    """Configure temp media directory for tests."""
    overrides = override_settings(
        MEDIA_ROOT=str(tmpdir_factory.mktemp('test_media')))
    overrides.enable()
