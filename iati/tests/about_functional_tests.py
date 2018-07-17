"""A module of functional tests for the about page and its sub pages.

TODO:
    Refactor most of these tests out into base functional tests.

"""
import os
from django.utils.text import slugify
import pytest
from base_functional_tests import TEST_DATA_DIR, click_obscured, view_live_page


ABOUT_PAGE = {
    'title': 'About',
    'heading': 'Test About Heading',
    'excerpt': 'This is an excerpt for the About page'
}
ABOUT_SUB_PAGE = {
    'page_type': 'About sub page',
    'title': 'test sub page',
    'heading': 'Test Sub Page',
    'excerpt': 'This is an excerpt for an About Sub page'
}
CASE_STUDY_INDEX_PAGE = {
    'page_type': 'Case study index page',
    'title': 'test case study index page',
    'heading': 'Test Case Study Index Page',
    'excerpt': 'This is an excerpt for a Case Study Index page'
}
HISTORY_PAGE = {
    'page_type': 'History page',
    'title': 'test history page',
    'heading': 'Test History Page',
    'excerpt': 'This is an excerpt for the History page'
}
PEOPLE_PAGE = {
    'page_type': 'People page',
    'title': 'test people page',
    'heading': 'Test People Page',
    'excerpt': 'This is an excerpt for the People page'
}
CASE_STUDY_PAGE = {
    'page_type': 'Case study page',
    'title': 'test case study page',
    'heading': 'Test Case Study Page',
    'excerpt': 'This is an excerpt for a Case Study page.'
}

H2 = {'content': 'H2 heading', 'button': 'H2', 'id': 'content_editor_en-{}-value'}
H3 = {'content': 'H3 heading', 'button': 'H3', 'id': 'content_editor_en-{}-value'}
H4 = {'content': 'H4 heading', 'button': 'H4', 'id': 'content_editor_en-{}-value'}


def navigate_to_default_page_cms_section(admin_browser, default_page_title):
    """Navigate to the About page section of the CMS.

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


def create_about_child_page(admin_browser, page_type, page_title):
    """Create a child page in the CMS.

    Args:
        page_type (str): The verbose name of the page model type you want to click on.
        page_title (str): The title of the page you are editing.

    """
    navigate_to_default_page_cms_section(admin_browser, 'About')
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
class TestAboutPage():
    """A container for tests to check functionality of About pages and child pages."""

    def test_can_edit_about_page_heading(self, admin_browser):
        """Check that an existing About page heading can be edited."""
        navigate_to_default_page_cms_section(admin_browser, 'About')
        edit_page_header(admin_browser, ABOUT_PAGE['title'], 'heading_en', ABOUT_PAGE['heading'])
        assert admin_browser.find_by_text(ABOUT_PAGE['heading'])

    def test_can_edit_about_page_excerpt(self, admin_browser):
        """Check that an existing About page excerpt can be edited."""
        edit_page_header(admin_browser, ABOUT_PAGE['title'], 'excerpt_en', ABOUT_PAGE['excerpt'])
        assert admin_browser.find_by_text(ABOUT_PAGE['excerpt'])

    @pytest.mark.parametrize('header', [
        H2,
        H3,
        H4
    ])
    def test_can_edit_about_page_with_header_text(self, admin_browser, header):
        """Check that an existing About page content editor can add a header."""
        admin_browser.find_by_text('About').click()
        admin_browser.find_by_text('English').click()
        element_count = admin_browser.find_by_id('content_editor_en-count').value
        scroll_to_bottom_of_page(admin_browser)
        reveal_content_editor(admin_browser, header['button'], element_count)
        admin_browser.find_by_text(header['button'])[int(element_count)].click()
        admin_browser.find_by_id(header['id'].format(element_count)).fill(header['content'])
        publish_page(admin_browser)
        view_live_page(admin_browser, 'About')
        assert admin_browser.is_text_present(header['content'])


@pytest.mark.django_db
class TestAboutChildPages():
    """A container for tests to check functionality of About child pages."""

    ABOUT_CHILD_PAGES = [
        ABOUT_SUB_PAGE,
        CASE_STUDY_INDEX_PAGE,
        HISTORY_PAGE,
        PEOPLE_PAGE
    ]

    @pytest.mark.parametrize('child_page', ABOUT_CHILD_PAGES)
    def test_can_create_about_child_pages(self, admin_browser, child_page):
        """Check that when an about child page is created it appears in the website."""
        create_about_child_page(admin_browser, child_page['page_type'], child_page['title'])
        view_live_page(admin_browser, child_page['title'])
        assert not admin_browser.is_text_present('Home')
        assert admin_browser.is_text_present(child_page['title'])

    @pytest.mark.parametrize('child_page', ABOUT_CHILD_PAGES)
    def test_can_edit_about_child_page_heading(self, admin_browser, child_page):
        """Check that About child page headings can be edited."""
        edit_page_header(admin_browser, child_page['title'], 'heading_en', child_page['heading'])
        assert admin_browser.find_by_text(child_page['heading'])

    @pytest.mark.parametrize('child_page', ABOUT_CHILD_PAGES)
    def test_can_edit_about_child_page_excerpt(self, admin_browser, child_page):
        """Check that About child page excerpts can be edited."""
        edit_page_header(admin_browser, child_page['title'], 'excerpt_en', child_page['excerpt'])
        assert admin_browser.find_by_text(child_page['excerpt'])

    @pytest.mark.parametrize('child_page', [
        ABOUT_SUB_PAGE,
        HISTORY_PAGE,
        PEOPLE_PAGE
    ])
    @pytest.mark.parametrize('header', [
        H2,
        H3,
        H4
    ])
    def test_can_edit_about_child_page_with_header_text(self, admin_browser, header, child_page):
        """Check that an About child page content editor can add a header."""
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


@pytest.mark.django_db
class TestCaseStudyPage():
    """A container for tests to check the ability to create Case Study pages."""

    CASE_STUDY_INDEX_PAGE_TITLE = 'test case study index page 2'

    def setup_case_study_index_page(self, admin_browser):
        """Create a Case Study Index page as a child of the About page."""
        create_about_child_page(admin_browser, CASE_STUDY_INDEX_PAGE['page_type'], self.CASE_STUDY_INDEX_PAGE_TITLE)

    def test_no_case_studies_section_on_home(self, admin_browser):
        """Before any case studies are published, test to see there is no Case studies section on the home page."""
        admin_browser.visit(os.environ['LIVE_SERVER_URL'])
        assert not admin_browser.is_text_present("Case studies")

    def test_can_create_case_study_page(self, admin_browser):
        """Check that a Case Study page can be created as a child of the Case Study Index page."""
        self.setup_case_study_index_page(admin_browser)
        admin_browser.find_by_xpath('//td[@class="no-children"]').click()
        enter_page_content(admin_browser, 'English', 'title_en', CASE_STUDY_PAGE['title'])
        enter_page_content(admin_browser, 'Promote', 'slug_en', slugify(CASE_STUDY_PAGE['title']))
        publish_page(admin_browser)
        view_live_page(admin_browser, CASE_STUDY_PAGE['title'])
        assert admin_browser.is_text_present(CASE_STUDY_PAGE['title'])

    def test_case_studies_section_on_home(self, admin_browser):
        """After one case study is published, check to see that the Case studies section has now appeared."""
        admin_browser.visit(os.environ['LIVE_SERVER_URL'])
        assert admin_browser.is_text_present("Case studies")

    def test_can_edit_case_study_page_heading(self, admin_browser):
        """Check that Case Study page headings can be edited."""
        edit_page_header(admin_browser, CASE_STUDY_PAGE['title'], 'heading_en', CASE_STUDY_PAGE['heading'])
        assert admin_browser.find_by_text(CASE_STUDY_PAGE['heading'])

    def test_can_edit_case_study_page_excerpt(self, admin_browser):
        """Check that Case Study page excerpts can be edited."""
        edit_page_header(admin_browser, CASE_STUDY_PAGE['title'], 'excerpt_en', CASE_STUDY_PAGE['excerpt'])
        assert admin_browser.find_by_text(CASE_STUDY_PAGE['excerpt'])

    @pytest.mark.parametrize('header', [
        H2,
        H3,
        H4
    ])
    def test_can_edit_case_study_page_with_header_text(self, admin_browser, header):
        """Check that an About child page content editor can add a header."""
        admin_browser.find_by_text(CASE_STUDY_PAGE['title']).click()
        admin_browser.find_by_text('English').click()
        scroll_to_bottom_of_page(admin_browser)
        element_count = admin_browser.find_by_id('content_editor_en-count').value
        reveal_content_editor(admin_browser, header['button'], element_count)
        admin_browser.find_by_text(header['button'])[int(element_count)].click()
        admin_browser.find_by_id(header['id'].format(element_count)).fill(header['content'])
        publish_page(admin_browser)
        view_live_page(admin_browser, CASE_STUDY_PAGE['title'])
        assert admin_browser.is_text_present(header['content'])

    def upload_an_image(self, admin_browser):
        """Upload an image in the CMS.

        Note:
            This is a duplicate function from base_functional_tests.

        """
        admin_browser.find_by_text('Choose an image').click()
        click_obscured(admin_browser, admin_browser.find_by_text('Upload').first)
        admin_browser.fill('title', 'Test image')
        admin_browser.attach_file('file', TEST_DATA_DIR + 'pigeons.jpeg')
        admin_browser.find_by_xpath('//em[contains(text(), "Upload")]').click()

    def test_feed_image_shows_on_index_page(self, admin_browser):
        """Check that when a user adds a feed image it also becomes the header image."""
        admin_browser.find_by_text(CASE_STUDY_PAGE['title']).click()
        self.upload_an_image(admin_browser)
        publish_page(admin_browser)
        view_live_page(admin_browser, self.CASE_STUDY_INDEX_PAGE_TITLE)
        header_image = admin_browser.find_by_xpath('//div[@class="case-study__media background-cover"]')
        assert 'pigeons' in header_image.outer_html

    def test_feed_image_shows_in_page_header(self, admin_browser):
        """Check that when a user adds a feed image it also becomes the header image.

        Note:
            This test currently requires the previous test to run due to lack of test isolation.

        """
        case_study_page_live_button = admin_browser.find_by_text('Live').first
        page_url = case_study_page_live_button._element.get_property('href')
        admin_browser.visit(page_url)
        header_image = admin_browser.find_by_xpath('//div[@class="hero hero--image"]')
        assert 'pigeons' in header_image.outer_html
