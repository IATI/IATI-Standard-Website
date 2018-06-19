"""A module of functional tests for the IATI Standard page."""
import pytest
from tests.base_functional_tests import click_obscured


def create_IATI_Standard_page(admin_browser):
    """Create an IATI Standard Page.

    TODO:
        Add line to click multilingual tab once editable header image branch gets merged in.

    """
    admin_browser.click_link_by_text('Pages')
    admin_browser.find_by_text('Home').click()
    admin_browser.click_link_by_text('Add child page')
    admin_browser.click_link_by_text('Iati standard page')
    admin_browser.fill('title_en', 'IATI standard')
    publish_changes(admin_browser)


def publish_changes(admin_browser):
    """Publish changes made in the CMS to the live page."""
    click_obscured(admin_browser, admin_browser.find_by_xpath('//div[@class="dropdown-toggle icon icon-arrow-up"]').first)
    click_obscured(admin_browser, admin_browser.find_by_text('Publish').first)


def view_live_page(admin_browser):
    """Visit the url of the 'View live' button so tests don't open a new window"""
    top_view_live_button = admin_browser.find_by_text('View live').first
    page_url = top_view_live_button._element.get_property('href')
    admin_browser.visit(page_url)


# I want to visit the IATI Standard page
@pytest.mark.django_db
class TestIATIStandardPageExists():
    """Container for tests that assert the existence of an IATI Standard page."""

    def test_IATI_Standard_page_exists(self, admin_browser):
        """Check there is an IATI Standard landing page."""
        create_IATI_Standard_page(admin_browser)
        view_live_page(admin_browser)
        assert admin_browser.title == 'IATI standard'


@pytest.mark.django_db
class TestIATIStandardPageisEditable():
    """Container for tests that an IATI Standard page is editable in expected ways."""

# I want to be able to edit the header text of this page
    def test_header_can_be_edited(self, admin_browser):
        """Check that the page header can be edited in the CMS."""
        admin_browser.find_by_text('IATI standard').click()
        admin_browser.fill('heading_en', 'IATI Standard')
        publish_changes(admin_browser)
        view_live_page(admin_browser)
        assert admin_browser.is_text_present('IATI Standard')

# I want to be able to edit the excerpt of this page
    def test_excerpt_can_be_edited(self, admin_browser):
        """Check that the page excerpt can be edited in the CMS."""
        admin_browser.find_by_text('IATI standard').click()
        admin_browser.fill('excerpt_en', 'This is an excerpt.')
        publish_changes(admin_browser)
        view_live_page(admin_browser)
        assert admin_browser.is_text_present('This is an excerpt.')
# I want to be able to edit the header image of this page
# I want to be able to add summary content to this page
# I want to be directed to the appropriate section of the site for me
# I want to be able to navigate to the appropriate page of the old Standard website
