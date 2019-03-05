"""A module of unit tests for redirects."""
import pytest
from django.conf import settings
from factories import DocumentFactory, ImageFactory


@pytest.mark.django_db
class TestRedirectMiddleware():

    def create_document(self):
        return DocumentFactory.create()

    def create_image(self):
        return ImageFactory.create()

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
        (settings.STATIC_URL + "MiXeDCaSe/", "/en" + settings.STATIC_URL + "MiXeDCaSe/")
    ])
    def test_redirect_middleware_default(self, client, redirect_mapping):
        response = client.get(redirect_mapping[0])
        assert response.url == redirect_mapping[1]

    def test_redirect_middleware_document(self, client):
        document = self.create_document()
        response = client.get(document.url)
        assert response.url == document.url

    def test_redirect_middleware_image(self, client):
        image = self.create_image()
        response = client.get(image.url)
        assert response.url == image.url
