"""A module of functional tests for the using data page and its sub pages.

TODO:
    Refactor most of these tests out into base functional tests.

"""
import os
from django.utils.text import slugify
import pytest
from base_functional_tests import TEST_DATA_DIR, click_obscured, view_live_page


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

H2 = {'content': 'H2 heading', 'button': 'H2', 'id': 'content_editor_en-{}-value'}
H3 = {'content': 'H3 heading', 'button': 'H3', 'id': 'content_editor_en-{}-value'}
H4 = {'content': 'H4 heading', 'button': 'H4', 'id': 'content_editor_en-{}-value'}


def navigate_to_default_page_cms_section(admin_browser, default_page_title):
    """Navigate to the Using data page section of the CMS.

    Args:
        default_page_title (str): The title of a default page modelself.

    """
    admin_browser.click_link_by_text('Pages')
    admin_browser.find_by_xpath('//span[@class="icon icon-arrow-right "]').click()
    admin_browser.find_by_text(default_page_title).click()


def enter_page_content(admin_browser, tab_name, cms_field, cms_content):
    """Add title and slug to a page in the CMS.

    Args:
        tab_name (str): The name of a tab on an edit page of the CMS.
        cms_field (str): The name of the field in the CMS you want to fill.
        cms_content (str): The text content you want to fill the field with.

    """
    admin_browser.find_by_text(tab_name).click()
    admin_browser.fill(cms_field, cms_content)


def publish_page(admin_browser):
    """Publish page created in the CMS.

    Note:
        Duplicate of publish_changes in base_functional_tests.

    """
    click_obscured(admin_browser, admin_browser.find_by_xpath('//div[@class="dropdown-toggle icon icon-arrow-up"]').first)
    click_obscured(admin_browser, admin_browser.find_by_text('Publish').first)


def create_using_data_child_page(admin_browser, page_type, page_title):
    """Create a child page in the CMS.

    Args:
        page_type (str): The verbose name of the page model type you want to click on.
        page_title (str): The title of the page you are editing.

    """
    navigate_to_default_page_cms_section(admin_browser, 'Using IATI data')
    admin_browser.find_by_text('Add child page').click()
    admin_browser.find_by_text(page_type).click()
    enter_page_content(admin_browser, 'English', 'title_en', page_title)
    enter_page_content(admin_browser, 'Promote', 'slug_en', slugify(page_title))
    publish_page(admin_browser)


def edit_page_header(admin_browser, page_title, cms_field, cms_content):
    """Edit a page by adding content via the CMS.

    Args:
        page_title (str): The title of the page you want to edit.
        cms_field (str): The name of the CMS field you want to enter content into.
        cms_content (str): The text content you want to add to the CMS field.

    TODO:
        Rename this function to avoid confusion with content editor tests.

    """
    admin_browser.find_by_text(page_title).click()
    enter_page_content(admin_browser, 'English', cms_field, cms_content)
    publish_page(admin_browser)
    view_live_page(admin_browser, page_title)


def scroll_to_bottom_of_page(admin_browser):
    """Scroll to the bottom of a page."""
    admin_browser.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def reveal_content_editor(admin_browser, button, element_count):
    """Open content editor if it is not already in view.

    Args:
        button (str): The displayed text name of the button you want to click.
        element_count (str): The element counter value of the content editor Streamfield block.

    TODO:
        Decide whether on convert element_count to int on assignment of variable.

    """
    if not admin_browser.find_by_text(button).visible:
        admin_browser.find_by_xpath('//div[@id="content_editor_en-{}-appendmenu"]/a'.format(int(element_count) - 1)).mouse_over()
        admin_browser.find_by_xpath('//div[@id="content_editor_en-{}-appendmenu"]/a'.format(int(element_count) - 1)).click()
        scroll_to_bottom_of_page(admin_browser)


@pytest.mark.django_db
class TestUsingDataPage():
    """A container for tests to check functionality of Using data pages and child pages."""

    def test_can_edit_using_data_page_heading(self, admin_browser):
        """Check that an existing Using data page heading can be edited."""
        navigate_to_default_page_cms_section(admin_browser, 'Using IATI data')
        edit_page_header(admin_browser, USING_DATA_PAGE['title'], 'heading_en', USING_DATA_PAGE['heading'])
        assert admin_browser.find_by_text(USING_DATA_PAGE['heading'])

    def test_can_edit_using_data_page_excerpt(self, admin_browser):
        """Check that an existing Using data page excerpt can be edited."""
        edit_page_header(admin_browser, USING_DATA_PAGE['title'], 'excerpt_en', USING_DATA_PAGE['excerpt'])
        assert admin_browser.find_by_text(USING_DATA_PAGE['excerpt'])

    @pytest.mark.parametrize('header', [
        H2,
        H3,
        H4
    ])
    def test_can_edit_using_data_page_with_header_text(self, admin_browser, header):
        """Check that an existing Using data page content editor can add a header."""
        admin_browser.find_by_text('Using IATI data').click()
        admin_browser.find_by_text('English').click()
        element_count = admin_browser.find_by_id('content_editor_en-count').value
        scroll_to_bottom_of_page(admin_browser)
        reveal_content_editor(admin_browser, header['button'], element_count)
        admin_browser.find_by_text(header['button'])[int(element_count)].click()
        admin_browser.find_by_id(header['id'].format(element_count)).fill(header['content'])
        publish_page(admin_browser)
        view_live_page(admin_browser, 'Using IATI data')
        assert admin_browser.is_text_present(header['content'])


@pytest.mark.django_db
class TestUsingDataChildPage():
    """A container for tests to check functionality of Using data child pages."""

    def test_can_create_using_data_child_pages(self, admin_browser):
        """Check that when a using data child page is created it appears in the website."""
        child_page = ABOUT_SUB_PAGE
        create_using_data_child_page(admin_browser, child_page['page_type'], child_page['title'])
        view_live_page(admin_browser, child_page['title'])
        assert not admin_browser.is_text_present('Home')
        assert admin_browser.is_text_present(child_page['title'])

    def test_can_edit_using_data_child_page_heading(self, admin_browser):
        """Check that Using data child page headings can be edited."""
        child_page = ABOUT_SUB_PAGE
        edit_page_header(admin_browser, child_page['title'], 'heading_en', child_page['heading'])
        assert admin_browser.find_by_text(child_page['heading'])

    def test_can_edit_using_data_child_page_excerpt(self, admin_browser):
        """Check that Using data child page excerpts can be edited."""
        child_page = ABOUT_SUB_PAGE
        edit_page_header(admin_browser, child_page['title'], 'excerpt_en', child_page['excerpt'])
        assert admin_browser.find_by_text(child_page['excerpt'])

    @pytest.mark.parametrize('header', [
        H2,
        H3,
        H4
    ])
    def test_can_edit_using_data_child_page_with_header_text(self, admin_browser, header):
        """Check that an Using data child page content editor can add a header."""
        child_page = ABOUT_SUB_PAGE
        admin_browser.find_by_text(child_page['title']).click()
        admin_browser.find_by_text('English').click()
        scroll_to_bottom_of_page(admin_browser)
        element_count = admin_browser.find_by_id('content_editor_en-count').value
        reveal_content_editor(admin_browser, header['button'], element_count)
        admin_browser.find_by_text(header['button'])[int(element_count)].click()
        admin_browser.find_by_id(header['id'].format(element_count)).fill(header['content'])
        publish_page(admin_browser)
        view_live_page(admin_browser, child_page['title'])
        assert admin_browser.is_text_present(header['content'])
