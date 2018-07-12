"""A module of functional tests for the using data page and its sub pages.

TODO:
    Refactor most of these tests out into base functional tests.

"""
import pytest
from tests import helper_functions


USING_DATA_PAGE = {
    'title': 'Using IATI data',
    'heading': 'Test using data Heading',
    'excerpt': 'This is an excerpt for the using data page'
}
ABOUT_SUB_PAGE = {
    'page_type': 'About sub page',
    'title': 'test sub page',
    'heading': 'Test Sub Page',
    'excerpt': 'This is an excerpt for an About Sub page'
}


@pytest.mark.django_db
class TestUsingDataPage():
    """A container for tests to check functionality of Using data pages and child pages."""

    def test_can_edit_using_data_page_heading(self, admin_browser):
        """Check that an existing Using data page heading can be edited."""
        helper_functions.navigate_to_default_page_cms_section(admin_browser, 'Using IATI data')
        helper_functions.edit_page_header(admin_browser, USING_DATA_PAGE['title'], 'heading_en', USING_DATA_PAGE['heading'])
        assert admin_browser.find_by_text(USING_DATA_PAGE['heading'])

    def test_can_edit_using_data_page_excerpt(self, admin_browser):
        """Check that an existing Using data page excerpt can be edited."""
        helper_functions.edit_page_header(admin_browser, USING_DATA_PAGE['title'], 'excerpt_en', USING_DATA_PAGE['excerpt'])
        assert admin_browser.find_by_text(USING_DATA_PAGE['excerpt'])


@pytest.mark.django_db
class TestUsingDataChildPage():
    """A container for tests to check functionality of Using data child pages."""

    def test_can_create_using_data_child_pages(self, admin_browser):
        """Check that when a using data child page is created it appears in the website."""
        child_page = ABOUT_SUB_PAGE
        helper_functions.create_using_data_child_page(admin_browser, child_page['page_type'], child_page['title'])
        helper_functions.view_live_page(admin_browser, child_page['title'])
        assert not admin_browser.is_text_present('Home')
        assert admin_browser.is_text_present(child_page['title'])

    def test_can_edit_using_data_child_page_heading(self, admin_browser):
        """Check that Using data child page headings can be edited."""
        child_page = ABOUT_SUB_PAGE
        helper_functions.edit_page_header(admin_browser, child_page['title'], 'heading_en', child_page['heading'])
        assert admin_browser.find_by_text(child_page['heading'])

    def test_can_edit_using_data_child_page_excerpt(self, admin_browser):
        """Check that Using data child page excerpts can be edited."""
        child_page = ABOUT_SUB_PAGE
        helper_functions.edit_page_header(admin_browser, child_page['title'], 'excerpt_en', child_page['excerpt'])
        assert admin_browser.find_by_text(child_page['excerpt'])
