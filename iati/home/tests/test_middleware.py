"""A module of unit tests for redirects."""
import pytest
from django.conf import settings
from factories import DocumentFactory


@pytest.mark.django_db
class TestRedirectMiddleware():
    """Tests for the custom redirect middleware."""

    def create_document(self):
        """Call the DocumentFactory to save a new document."""
        return DocumentFactory.create()

    @pytest.mark.parametrize('redirect_mapping', [
        ('/HoMe/', '/home/'),
        ('/HOME/', '/home/'),
        ('/home/', '/en/home/'),
        ('/104/MiXeDCaSe/', 'http://reference.iatistandard.org/104/MiXeDCaSe/'),
        ('/105/MiXeDCaSe/', 'http://reference.iatistandard.org/105/MiXeDCaSe/'),
        ('/201/MiXeDCaSe/', 'http://reference.iatistandard.org/201/MiXeDCaSe/'),
        ('/202/MiXeDCaSe/', 'http://reference.iatistandard.org/202/MiXeDCaSe/'),
        ('/203/MiXeDCaSe/', 'http://reference.iatistandard.org/203/MiXeDCaSe/'),
        ('/activity-standard/MiXeDCaSe/', 'http://reference.iatistandard.org/activity-standard/MiXeDCaSe/'),
        ('/codelists/MiXeDCaSe/', 'http://reference.iatistandard.org/codelists/MiXeDCaSe/'),
        ('/developer/MiXeDCaSe/', 'http://reference.iatistandard.org/developer/MiXeDCaSe/'),
        ('/introduction/MiXeDCaSe/', 'http://reference.iatistandard.org/introduction/MiXeDCaSe/'),
        ('/namespaces-extensions/MiXeDCaSe/', 'http://reference.iatistandard.org/namespaces-extensions/MiXeDCaSe/'),
        ('/organisation-identifiers/MiXeDCaSe/', 'http://reference.iatistandard.org/organisation-identifiers/MiXeDCaSe/'),
        ('/organisation-standard/MiXeDCaSe/', 'http://reference.iatistandard.org/organisation-standard/MiXeDCaSe/'),
        ('/reference/MiXeDCaSe/', 'http://reference.iatistandard.org/reference/MiXeDCaSe/'),
        ('/rulesets/MiXeDCaSe/', 'http://reference.iatistandard.org/rulesets/MiXeDCaSe/'),
        ('/schema/MiXeDCaSe/', 'http://reference.iatistandard.org/schema/MiXeDCaSe/'),
        ('/upgrades/MiXeDCaSe/', 'http://reference.iatistandard.org/upgrades/MiXeDCaSe/'),
        (settings.STATIC_URL + "HOME/css/", "/en" + settings.STATIC_URL + "HOME/css/")
    ])
    def test_redirect_middleware_default(self, client, redirect_mapping):
        """Test default behavior for redirects."""
        response = client.get(redirect_mapping[0])
        if response.status_code == 301:
            retry = client.get(response.url)
            assert retry.url == redirect_mapping[1]
        assert response.url == redirect_mapping[1]

    def test_redirect_middleware_document(self, client):
        """Test that documents are excluded from the middleware."""
        document = self.create_document()
        response = client.get(document.url)
        assert response.status_code == 200
