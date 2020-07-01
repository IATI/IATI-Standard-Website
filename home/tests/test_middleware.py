"""A module of unit tests for redirects."""
import pytest
from django.conf import settings
from factories import DocumentFactory
from wagtail.core.models import Page
from about.models import AboutPage


@pytest.mark.django_db
class TestRedirectMiddleware():
    """Tests for the custom redirect middleware."""

    def create_document(self):
        """Call the DocumentFactory to save a new document."""
        return DocumentFactory.create()

    def test_redirect_middleware_internal(self, client):
        """
        Test behavior for internal redirects.

        Create about page not dependent on default pages being added
        via management command.
        """
        home = Page.objects.get(id=3)
        about = AboutPage(title='About us')
        home.add_child(instance=about)
        response = client.get('/About-Us', follow=True)
        assert response.status_code == 200

    @pytest.mark.parametrize('redirect_mapping', [
        ('/203/codelists/OtherIdentifierType/', 'https://iatistandard.org/en/iati-standard/203/codelists/otheridentifiertype/'),
        ('/schema/downloads/CHANGES.txt', 'https://iatistandard.org/downloads/203/schema/downloads/changes.txt'),
        ('/developer/test_slug_here', 'https://iatistandard.org/en/guidance/developer/')
    ])
    def test_redirect_middleware_external(self, client, redirect_mapping):
        """Test behavior for external redirects."""
        response = client.get(redirect_mapping[0])
        assert response.url == redirect_mapping[1]

    @pytest.mark.parametrize('redirect_mapping', [
        ("{}HOME/css/".format(settings.STATIC_URL), "/en{}HOME/css/".format(settings.STATIC_URL))
    ])
    def test_redirect_middleware_static(self, client, redirect_mapping):
        """Test behavior for static pages going through the middleware."""
        response = client.get(redirect_mapping[0])
        assert response.url == redirect_mapping[1]

    def test_redirect_middleware_document(self, client):
        """Test that documents are excluded from the middleware."""
        document = self.create_document()
        response = client.get(document.url)
        assert response.status_code == 200
