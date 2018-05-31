"""A module of functional tests for the home page."""
import pytest
from tests.base_functional_tests import click_obscured

HOME_PAGE = {
    'title': 'Home',
    'heading': 'Test International Aid Transparency Initiative',
    'excerpt': 'This is an excerpt for the Home page'
}


@pytest.mark.django_db
class TestHomePage():
    """A container for tests to check functionality of the Home Page."""

    def navigate_to_edit_home_page(self, admin_browser):
        """Navigate to the editable section of the CMS for the Home Page."""
        admin_browser.click_link_by_text('Pages')
        admin_browser.find_by_xpath('//h3').find_by_text('Home').click()
        admin_browser.click_link_by_text('Home')

    def publish_changes(self, admin_browser):
        """Publish changes made in the CMS to the live page."""
        click_obscured(admin_browser, admin_browser.find_by_xpath('//div[@class="dropdown-toggle icon icon-arrow-up"]').first)
        click_obscured(admin_browser, admin_browser.find_by_text('Publish').first)

    def view_live_page(self, admin_browser):
        """Visit the url of the 'View live' button so tests don't open a new window"""
        top_view_live_button = admin_browser.find_by_text('View live').first
        page_url = top_view_live_button._element.get_property('href')
        admin_browser.visit(page_url)

    def test_can_edit_home_page_heading(self, admin_browser):
        """Check that the Home page heading can be edited."""
        self.navigate_to_edit_home_page(admin_browser)
        # Click the English tab
        admin_browser.find_by_text('English').click()
        # Fill the heading field
        admin_browser.fill('heading_en', HOME_PAGE['heading'])
        # Publish new page heading
        self.publish_changes(admin_browser)
        self.view_live_page(admin_browser)
        assert admin_browser.find_by_text(HOME_PAGE['heading'])

    def test_can_edit_home_page_excerpt(self, admin_browser):
        """Check that the Home page excerpt can be edited."""
        self.navigate_to_edit_home_page(admin_browser)
        # Click the English tab
        admin_browser.find_by_text('English').click()
        # Fill the excerpt field
        admin_browser.fill('excerpt_en', HOME_PAGE['excerpt'])
        # Publish new page excerpt
        self.publish_changes(admin_browser)
        self.view_live_page(admin_browser)
        assert admin_browser.find_by_text(HOME_PAGE['excerpt'])
