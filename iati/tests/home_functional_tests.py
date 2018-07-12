"""A module of functional tests for the home page."""
import pytest
from tests import helper_functions


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

    def test_can_edit_home_page_heading(self, admin_browser):
        """Check that the Home page heading can be edited."""
        self.navigate_to_edit_home_page(admin_browser)
        # Click the English tab
        admin_browser.find_by_text('English').click()
        # Fill the heading field
        admin_browser.fill('heading_en', HOME_PAGE['heading'])
        # Publish new page heading
        helper_functions.publish_changes(admin_browser)
        helper_functions.view_live_page(admin_browser, HOME_PAGE['title'])
        assert admin_browser.find_by_text(HOME_PAGE['heading'])

    def test_can_edit_home_page_excerpt(self, admin_browser):
        """Check that the Home page excerpt can be edited."""
        self.navigate_to_edit_home_page(admin_browser)
        # Click the English tab
        admin_browser.find_by_text('English').click()
        # Fill the excerpt field
        admin_browser.fill('excerpt_en', HOME_PAGE['excerpt'])
        # Publish new page excerpt
        helper_functions.publish_changes(admin_browser)
        helper_functions.view_live_page(admin_browser, HOME_PAGE['title'])
        assert admin_browser.find_by_text(HOME_PAGE['excerpt'])


PRIVACY_PAGE = {
    'page_type': 'Standard page',
    'fixed_page_type': 'privacy',
    'title': 'Privacy page',
    'heading': 'Privacy page header',
    'base_link_text': 'Privacy policy'
}
TERMS_PAGE = {
    'page_type': 'Standard page',
    'fixed_page_type': 'terms',
    'title': 'Terms and conditions page',
    'heading': 'Terms and conditions page header',
    'base_link_text': 'Terms and conditions'
}


@pytest.mark.django_db
class TestFixedStandardPages():
    """Tests to see if fixed standard pages are properly linked"""
    @pytest.mark.parametrize('fixed_page', [
        PRIVACY_PAGE,
        TERMS_PAGE
    ])
    def test_can_create_standard_pages(self, admin_browser, fixed_page):
        """Check that when an event index child page is created it appears in the website."""
        helper_functions.create_standard_home_page(admin_browser, fixed_page['page_type'], fixed_page['fixed_page_type'], fixed_page['title'])
        helper_functions.view_live_page(admin_browser, fixed_page['title'])
        assert admin_browser.title == fixed_page['title']
        admin_browser.click_link_by_text(fixed_page['base_link_text'])
        assert admin_browser.title == fixed_page['title']
