"""A module of functional tests for the IATI Standard page."""
import pytest
from tests.base_functional_tests import click_obscured
from tests.about_functional_tests import reveal_content_editor, scroll_to_bottom_of_page


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
        """Check that the page header can be edited in the CMS.

        TODO:
            Add line to click multilingual tab once editable header image branch gets merged in.

        """
        admin_browser.find_by_text('IATI standard').click()
        admin_browser.fill('heading_en', 'IATI Standard')
        publish_changes(admin_browser)
        view_live_page(admin_browser)
        assert admin_browser.is_text_present('IATI Standard')

# I want to be able to edit the excerpt of this page
    def test_excerpt_can_be_edited(self, admin_browser):
        """Check that the page excerpt can be edited in the CMS.

        TODO:
            Add line to click multilingual tab once editable header image branch gets merged in.

        """
        admin_browser.find_by_text('IATI standard').click()
        admin_browser.fill('excerpt_en', 'This is an excerpt.')
        publish_changes(admin_browser)
        view_live_page(admin_browser)
        assert admin_browser.is_text_present('This is an excerpt.')
# I want to be able to edit the header image of this page - awiting merging of PR#129

# I want to be able to add summary content to this page
    def test_body_content_can_be_edited_simple(self, admin_browser):
        """Check that basic text content from the content editor in the CMS shows on the page.

        TODO:
            Add line to click multilingual tab once editable header image branch gets merged in.

        """
        admin_browser.find_by_text('IATI standard').click()
        element_count = admin_browser.find_by_id('content_editor_en-count').value
        scroll_to_bottom_of_page(admin_browser)
        reveal_content_editor(admin_browser, 'Intro', element_count)
        admin_browser.find_by_text('Intro')[int(element_count)].click()
        admin_browser.find_by_xpath('//div[@class="notranslate public-DraftEditor-content"]').fill('This is some content.')
        publish_changes(admin_browser)
        view_live_page(admin_browser)
        assert admin_browser.is_text_present('This is some content.')


# I want to be directed to the appropriate section of the old IATI standard site for me
# @pytest.mark.django_db
# class TestRedirectLinksWorking():
#     """Container for tests that check redirects are correct and working."""
#
#     ORG_STANDARD = {'id': 'org-standard', 'expected_content': 'This section details the IATI Organisation standard.'}
#
#     HARDCODED_LINKS = [ORG_STANDARD]
#
#     @pytest.mark.parametrize('link', HARDCODED_LINKS)
#     def test_hardcoded_links_work(self, admin_browser, link):
#         """Check that the given link goes to the correct page."""
#         admin_browser
