"""A module of functional tests for the events index page and events/past events pages.

TODO:
    Refactor most of these tests out into base functional tests.

"""
import os
import pytest
from django.utils.text import slugify
from base_functional_tests import find_and_click_add_button, find_and_click_toggle_button, fill_content_editor_block
import pdb


EVENT_INDEX_PAGE = {
    'title': 'Events',
    'heading': 'Test IATI Events',
    'excerpt': 'This is an excerpt for the Event Index Page'
}
EVENT_PAGE = {
    'page_type': 'Event page',
    'title': 'test event page',
    'heading': 'Test Event Page Heading',
    'excerpt': 'This is an excerpt for an Test Event page'
}

H2 = {'content': 'H2 heading', 'button': 'H2', 'id': 'content_editor_en-{}-value'}
H3 = {'content': 'H3 heading', 'button': 'H3', 'id': 'content_editor_en-{}-value'}
H4 = {'content': 'H4 heading', 'button': 'H4', 'id': 'content_editor_en-{}-value'}


def navigate_to_default_page_cms_section(admin_browser, default_page_title):
    """Navigate to the Event page section of the CMS.

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
    tab = admin_browser.find_by_text(tab_name)
    _ = tab[0].__dict__['_element'].location_once_scrolled_into_view
    tab[0].click()
    elem = admin_browser.find_by_css("[name='{}']".format(cms_field))
    _ = elem[0].__dict__['_element'].location_once_scrolled_into_view
    admin_browser.fill(cms_field, cms_content)


def publish_page(admin_browser):
    """Publish page created in the CMS."""
    admin_browser.find_by_xpath('//div[@class="dropdown-toggle icon icon-arrow-up"]').click()
    admin_browser.find_by_text('Publish').click()


def create_event_child_page(admin_browser, page_type, page_title):
    """Create a child page in the CMS.

    Args:
        page_type (str): The verbose name of the page model type you want to click on.
        page_title (str): The title of the page you are editing.

    """
    navigate_to_default_page_cms_section(admin_browser, 'Events')
    admin_browser.find_by_text('Add child page').click()
    admin_browser.find_by_text(page_type).click()
    admin_browser.find_by_css(".xdsoft_next")[0].click()
    admin_browser.find_by_css(".xdsoft_day_of_week3")[0].click()
    enter_page_content(admin_browser, 'English', 'title_en', page_title)
    enter_page_content(admin_browser, 'Promote', 'slug_en', slugify(page_title))
    publish_page(admin_browser)


def view_live_page(admin_browser, page_title):
    """Navigate to the published page on the site.

    Args:
        page_title (str): The page title text you are expecting on the live page.

    """
    button_links = admin_browser.find_by_xpath('//a[@title="View live version of \'{}\'"]'.format(page_title))
    href = button_links[0].__dict__['_element'].get_property('href')
    admin_browser.visit(href)


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
    if not admin_browser.find_by_text(button).visible and int(element_count) > 0:
        toggle = admin_browser.find_by_xpath('//div[@id="content_editor_en-{}-appendmenu"]/a'.format(int(element_count) - 1))[0]
        admin_browser.driver.execute_script("arguments[0].click();", toggle.__dict__['_element'])
        scroll_to_bottom_of_page(admin_browser)


@pytest.mark.django_db
class TestEventPage():
    """A container for tests to check functionality of Event pages and child pages."""

    def test_can_edit_event_page_heading(self, admin_browser):
        """Check that an existing Event page heading can be edited."""
        navigate_to_default_page_cms_section(admin_browser, 'Events')
        edit_page_header(admin_browser, EVENT_INDEX_PAGE['title'], 'heading_en', EVENT_INDEX_PAGE['heading'])
        assert admin_browser.find_by_text(EVENT_INDEX_PAGE['heading'])

    def test_events_past_parameter(self, admin_browser):
        admin_browser.visit(os.environ['LIVE_SERVER_URL'] + "/admin/pages/3/")
        view_live_page(admin_browser, EVENT_INDEX_PAGE['title'])
        assert admin_browser.is_element_not_present_by_text("Past {}".format(EVENT_INDEX_PAGE['heading']))
        admin_browser.visit(admin_browser.url + "?past=1")
        assert admin_browser.find_by_text("Past {}".format(EVENT_INDEX_PAGE['heading']))

    def test_can_edit_event_page_excerpt(self, admin_browser):
        """Check that an existing Event page excerpt can be edited."""
        edit_page_header(admin_browser, EVENT_INDEX_PAGE['title'], 'excerpt_en', EVENT_INDEX_PAGE['excerpt'])
        assert admin_browser.find_by_text(EVENT_INDEX_PAGE['excerpt'])


@pytest.mark.django_db
class TestEventIndexChildPages():
    """A container for tests to check functionality of Event Index child pages."""

    def test_can_create_event_child_pages(self, admin_browser):
        """Check that when an event index child page is created it appears in the website."""
        create_event_child_page(admin_browser, EVENT_PAGE['page_type'], EVENT_PAGE['title'])
        view_live_page(admin_browser, EVENT_PAGE['title'])
        assert not admin_browser.is_text_present('Home')
        assert admin_browser.title == EVENT_PAGE['title']

    def test_can_edit_event_child_page_heading(self, admin_browser):
        """Check that Event index child page headings can be edited."""
        edit_page_header(admin_browser, EVENT_PAGE['title'], 'heading_en', EVENT_PAGE['heading'])
        assert admin_browser.find_by_text(EVENT_PAGE['heading'])

    def test_can_edit_event_child_page_excerpt(self, admin_browser):
        """Check that Event index child page excerpts can be edited."""
        edit_page_header(admin_browser, EVENT_PAGE['title'], 'excerpt_en', EVENT_PAGE['excerpt'])
        assert admin_browser.find_by_text(EVENT_PAGE['excerpt'])

    @pytest.mark.parametrize('header', [
        H2,
        H3,
        H4
    ])
    def test_can_edit_event_child_page_with_header_text(self, admin_browser, header):
        """Check that an Event index child page content editor can add a header."""
        admin_browser.find_by_text(EVENT_PAGE['title'])[0].click()
        admin_browser.find_by_text('English')[0].click()
        find_and_click_toggle_button(admin_browser, 0)
        find_and_click_add_button(admin_browser, header['button'].lower())
        fill_content_editor_block(admin_browser, header['button'].lower(), " input", header['content'])
        # scroll_to_bottom_of_page(admin_browser)
        # element_count = admin_browser.find_by_id('content_editor_en-count').value
        # reveal_content_editor(admin_browser, header['button'], element_count)
        # admin_browser.find_by_text(header['button'])[int(element_count)].click()
        # admin_browser.find_by_id(header['id'].format(element_count)).fill(header['content'])
        publish_page(admin_browser)
        view_live_page(admin_browser, EVENT_PAGE['title'])
        assert admin_browser.is_text_present(header['content'])
