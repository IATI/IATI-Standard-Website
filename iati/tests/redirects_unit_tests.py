"""A module of unit tests for redirects."""
import pytest


@pytest.mark.django_db
class TestRedirectLinksWorking():
    """Container for tests that check redirects are correct and working."""

    @pytest.mark.parametrize('redirect_mapping', [
        ('/101/', 'http://reference.iatistandard.org/101/'),
        ('/102/', 'http://reference.iatistandard.org/102/'),
        ('/103/', 'http://reference.iatistandard.org/103/'),
        ('/104/', 'http://reference.iatistandard.org/104/'),
        ('/105/', 'http://reference.iatistandard.org/105/'),
        ('/201/', 'http://reference.iatistandard.org/201/'),
        ('/202/', 'http://reference.iatistandard.org/202/'),
        ('/203/', 'http://reference.iatistandard.org/203/'),
        ('/activity-standard/', 'http://reference.iatistandard.org/activity-standard/'),
        ('/codelists/', 'http://reference.iatistandard.org/codelists/'),
        ('/developer/', 'http://reference.iatistandard.org/developer/'),
        ('/introduction/', 'http://reference.iatistandard.org/introduction/'),
        ('/namespaces-extensions/', 'http://reference.iatistandard.org/namespaces-extensions/'),
        ('/organisation-identifiers/', 'http://reference.iatistandard.org/organisation-identifiers/'),
        ('/organisation-standard/', 'http://reference.iatistandard.org/organisation-standard/'),
        ('/reference/', 'http://reference.iatistandard.org/reference/'),
        ('/rulesets/', 'http://reference.iatistandard.org/rulesets/'),
        ('/schema/', 'http://reference.iatistandard.org/schema/'),
        ('/upgrades/', 'http://reference.iatistandard.org/upgrades/'),
    ])
    def test_basic_redirects_work(self, client, redirect_mapping):
        """Check that the given links redirect."""
        response = client.get(redirect_mapping[0])
        assert response.status_code == 301
        assert response.url == redirect_mapping[1]

    @pytest.mark.parametrize('redirect_mapping', [
        ('/203/codelists/', 'http://reference.iatistandard.org/203/codelists/'),
        ('/203/codelists/AidType/', 'http://reference.iatistandard.org/203/codelists/AidType/'),
    ])
    def test_descendent_redirects_work(self, client, redirect_mapping):
        """Check that descendent paths are also redirected."""
        response = client.get(redirect_mapping[0])
        assert response.status_code == 301
        assert response.url == redirect_mapping[1]
