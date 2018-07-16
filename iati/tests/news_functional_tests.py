"""A module of functional tests for the news index page and news pages.

TODO:
    Refactor most of these tests out into base functional tests.

"""
import pytest
from django.utils.text import slugify
from base_functional_tests import find_and_click_add_button, find_and_click_toggle_button, fill_content_editor_block, view_live_page
# from base_functional_tests import click_obscured
# from iati.urls import ADMIN_SLUG


NEWS_INDEX_PAGE = {
    'title': 'News',
    'heading': 'Test IATI news',
    'excerpt': 'This is an excerpt for the News Index Page'
}
NEWS_PAGE = {
    'page_type': 'News page',
    'title': 'test news page',
    'heading': 'Test news Page Heading',
}

TEST_CATEGORY = "Test IATI news category"

H2 = {'content': 'H2 heading', 'button': 'Heading 2', 'id': 'content_editor_en-{}-value'}
H3 = {'content': 'H3 heading', 'button': 'Heading 3', 'id': 'content_editor_en-{}-value'}
H4 = {'content': 'H4 heading', 'button': 'Heading 4', 'id': 'content_editor_en-{}-value'}


def navigate_to_default_page_cms_section(admin_browser, default_page_title):
    """Navigate to the news page section of the CMS.

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


def create_news_child_page(admin_browser, page_type, page_title):
    """Create a child page in the CMS.

    Args:
        page_type (str): The verbose name of the page model type you want to click on.
        page_title (str): The title of the page you are editing.

    """
    navigate_to_default_page_cms_section(admin_browser, 'News')
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
    if not admin_browser.find_by_text(button).visible and int(element_count) > 0:
        toggle = admin_browser.find_by_xpath('//div[@id="content_editor_en-{}-appendmenu"]/a'.format(int(element_count) - 1))[0]
        admin_browser.driver.execute_script("arguments[0].click();", toggle.__dict__['_element'])
        scroll_to_bottom_of_page(admin_browser)


@pytest.mark.django_db
class TestNewsPage():
    """A container for tests to check functionality of news pages and child pages."""

    def test_can_edit_news_page_heading(self, admin_browser):
        """Check that an existing news page heading can be edited."""
        navigate_to_default_page_cms_section(admin_browser, 'News')
        edit_page_header(admin_browser, NEWS_INDEX_PAGE['title'], 'heading_en', NEWS_INDEX_PAGE['heading'])
        assert admin_browser.find_by_text(NEWS_INDEX_PAGE['heading'])

    def test_can_edit_news_page_excerpt(self, admin_browser):
        """Check that an existing news page excerpt can be edited."""
        edit_page_header(admin_browser, NEWS_INDEX_PAGE['title'], 'excerpt_en', NEWS_INDEX_PAGE['excerpt'])
        assert admin_browser.find_by_text(NEWS_INDEX_PAGE['excerpt'])


@pytest.mark.django_db
class TestNewsIndexChildPages():
    """A container for tests to check functionality of news Index child pages."""

    def test_can_create_news_child_pages(self, admin_browser):
        """Check that when an news index child page is created it appears in the website."""
        create_news_child_page(admin_browser, NEWS_PAGE['page_type'], NEWS_PAGE['title'])
        view_live_page(admin_browser, NEWS_PAGE['title'])
        assert not admin_browser.is_text_present('Home')
        assert admin_browser.title == NEWS_PAGE['title']

    def test_can_edit_news_child_page_heading(self, admin_browser):
        """Check that news index child page headings can be edited."""
        edit_page_header(admin_browser, NEWS_PAGE['title'], 'heading_en', NEWS_PAGE['heading'])
        assert admin_browser.find_by_text(NEWS_PAGE['heading'])

    @pytest.mark.parametrize('header', [
        H2,
        H3,
        H4
    ])
    def test_can_edit_news_child_page_with_header_text(self, admin_browser, header):
        """Check that an news index child page content editor can add a header."""
        admin_browser.find_by_text(NEWS_PAGE['title'])[0].click()
        admin_browser.find_by_text('English')[0].click()
        find_and_click_toggle_button(admin_browser, 0)
        header_class = header['button'].lower().replace(' ', '_')
        find_and_click_add_button(admin_browser, header_class)
        fill_content_editor_block(admin_browser, header_class, " input", header['content'])
        publish_page(admin_browser)
        view_live_page(admin_browser, NEWS_PAGE['title'])
        assert admin_browser.is_text_present(header['content'])
    # TODO: Find out why this is consistently failing
    # def test_news_category_filter(self, admin_browser):
    #     """Create a news category, assign it to 4 child pages, and test param"""
    #     admin_browser.visit(os.environ['LIVE_SERVER_URL'] + '/{}/'.format(ADMIN_SLUG))
    #     admin_browser.click_link_by_text("Snippets")
    #     click_obscured(admin_browser, admin_browser.find_by_xpath("//a[contains(normalize-space(.), 'News categories')]")[0])
    #     admin_browser.click_link_by_text("Add news category")
    #     admin_browser.fill("name_en", TEST_CATEGORY)
    #     admin_browser.find_by_css(".action-save").click()
    #     for i in range(0, 4):
    #         navigate_to_default_page_cms_section(admin_browser, 'News')
    #         admin_browser.find_by_text('Add child page').click()
    #         admin_browser.find_by_id('id_date').click()
    #         admin_browser.check('news_categories')
    #         enter_page_content(admin_browser, 'English', 'title_en', NEWS_PAGE['title'] + str(i))
    #         enter_page_content(admin_browser, 'Promote', 'slug_en', slugify(NEWS_PAGE['title'] + str(i)))
    #         publish_page(admin_browser)
    #     navigate_to_default_page_cms_section(admin_browser, 'News')
    #     view_live_page(admin_browser, NEWS_INDEX_PAGE['title'])
    #     assert admin_browser.is_element_present_by_text('1 / 2')
    #     admin_browser.click_link_by_text(TEST_CATEGORY)
    #     assert admin_browser.is_element_present_by_text("Show all posts")
