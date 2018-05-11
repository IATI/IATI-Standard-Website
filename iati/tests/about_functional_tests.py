"""A module of functional tests for the about page and its sub pages."""
from django.utils.text import slugify
import pytest


def navigate_to_about_cms(admin_browser):
    """Navigate to the About page section of the CMS."""
    admin_browser.click_link_by_text('Pages')
    admin_browser.find_by_xpath('//*[@class="icon icon-arrow-right "]').click()
    admin_browser.find_by_text('About').click()


def create_a_child_page(admin_browser, page_type, page_title):
    """Create a child page in the CMS."""
    admin_browser.find_by_text('Add child page').click()
    admin_browser.find_by_text(page_type).click()
    admin_browser.find_by_text('English').click()
    admin_browser.fill('title_en', page_title)
    admin_browser.find_by_text('Promote').click()
    admin_browser.fill('slug_en', slugify(page_title))
    admin_browser.find_by_xpath('//*[@class="dropdown-toggle icon icon-arrow-up"]').click()
    admin_browser.find_by_text('Publish').click()


@pytest.mark.django_db()
class TestAboutChildPageCreation():
    """A container for tests to check the ability to create About child pages."""

    @pytest.mark.parametrize('child_page', [
        {'page_type': 'About sub page', 'title': 'test sub page'},
        {'page_type': 'Case study index page', 'title': 'test case study index page'},
        {'page_type': 'History page', 'title': 'test history page'},
        {'page_type': 'People page', 'title': 'test people page'}
    ])
    def test_can_create_about_child_pages(self, admin_browser, child_page):
        """Check that when an about child page is created it appears in the website."""
        navigate_to_about_cms(admin_browser)
        admin_browser.find_by_text('Add child page').click()
        admin_browser.find_by_text(child_page['page_type']).click()
        admin_browser.find_by_text('English').click()
        admin_browser.fill('title_en', child_page['title'])
        admin_browser.find_by_text('Promote').click()
        admin_browser.fill('slug_en', slugify(child_page['title']))
        admin_browser.find_by_xpath('//*[@class="dropdown-toggle icon icon-arrow-up"]').click()
        admin_browser.find_by_text('Publish').click()
        admin_browser.find_by_text(child_page['title']).mouse_over()
        admin_browser.find_by_text('View live').click()
        assert admin_browser.is_text_present(child_page['title'])


@pytest.mark.django_db()
class TestCaseStudyIndexChildPageCreation():
    """A container for tests to check the ability to create Case Study pages."""

    def setup_case_study_index_page(self, admin_browser):
        """Create a Case Study Index page as a child of the About page."""
        case_study_index_type = 'Case study index page'
        case_study_index_title = 'test case study index parent page'
        navigate_to_about_cms(admin_browser)


    def test_can_create_case_study_pages(self, admin_browser):
        """Check that a Case Study page can be created as a child of the Case Study Index page."""
        self.setup_case_study_index_page(admin_browser)
