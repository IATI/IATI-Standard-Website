"""A module of functional tests for the IATI Standard page."""
import pytest
from tests.base_functional_tests import click_obscured
from tests.about_functional_tests import reveal_content_editor, scroll_to_bottom_of_page, view_live_page


def navigate_to_Home_cms_section(admin_browser):
    """Navigate to the Home section of the CMS."""
    admin_browser.click_link_by_text('Pages')
    admin_browser.find_by_text('Home').click()


def publish_changes(admin_browser):
    """Publish changes made in the CMS to the live page."""
    click_obscured(admin_browser, admin_browser.find_by_xpath('//div[@class="dropdown-toggle icon icon-arrow-up"]').first)
    click_obscured(admin_browser, admin_browser.find_by_text('Publish').first)


@pytest.mark.django_db
class TestIATIStandardPageisEditable():
    """Container for tests that an IATI Standard page is editable in expected ways."""

# I want to be able to edit the header text of this page
    def test_header_can_be_edited(self, admin_browser):
        """Check that the page header can be edited in the CMS."""
        navigate_to_Home_cms_section(admin_browser)
        admin_browser.find_by_text('IATI Standard').click()
        admin_browser.find_by_text('English')[0].click()
        admin_browser.fill('heading_en', 'IATI Standard')
        publish_changes(admin_browser)
        view_live_page(admin_browser, 'IATI Standard')
        assert admin_browser.is_text_present('IATI Standard')

# I want to be able to edit the excerpt of this page
    def test_excerpt_can_be_edited(self, admin_browser):
        """Check that the page excerpt can be edited in the CMS."""
        navigate_to_Home_cms_section(admin_browser)
        admin_browser.find_by_text('IATI Standard').click()
        admin_browser.find_by_text('English')[0].click()
        admin_browser.fill('excerpt_en', 'This is an excerpt.')
        publish_changes(admin_browser)
        view_live_page(admin_browser, 'IATI Standard')
        assert admin_browser.is_text_present('This is an excerpt.')

# I want to be able to add summary content to this page
    def test_body_content_can_be_edited_simple(self, admin_browser):
        """Check that basic text content from the content editor in the CMS shows on the page."""
        navigate_to_Home_cms_section(admin_browser)
        admin_browser.find_by_text('IATI Standard').click()
        admin_browser.find_by_text('English')[0].click()
        element_count = admin_browser.find_by_id('content_editor_en-count').value
        scroll_to_bottom_of_page(admin_browser)
        reveal_content_editor(admin_browser, 'Intro', element_count)
        admin_browser.find_by_text('Intro')[int(element_count)].click()
        admin_browser.find_by_xpath('//div[@class="notranslate public-DraftEditor-content"]').fill('This is some content.')
        publish_changes(admin_browser)
        view_live_page(admin_browser, 'IATI Standard')
        assert admin_browser.is_text_present('This is some content.')
