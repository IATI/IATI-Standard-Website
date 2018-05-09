"""A module of functional tests for the about page and its sub pages."""
import pytest
from django.utils.text import slugify


@pytest.mark.ignore_template_errors
@pytest.mark.django_db()
class TestAboutChildPageCreation():
    """A container for tests to check the ability to creat About child pages."""

    @pytest.mark.parametrize('child_page', [
        {'page_type': 'About sub page', 'title': 'test sub page'},
        {'page_type': 'Case study index page', 'title': 'test case study index page'},
        {'page_type': 'History page', 'title': 'test history page'},
        {'page_type': 'People page', 'title': 'test people page'}
    ])
    def test_can_create_about_child_pages(self, admin_browser, child_page):
        """Check that expected about child pages can be created."""
        admin_browser.click_link_by_text('Pages')
        admin_browser.find_by_xpath('//*[@class="icon icon-arrow-right "]').click()
        admin_browser.find_by_text('About').click()
        admin_browser.find_by_text('Add child page').click()
        admin_browser.find_by_text(child_page['page_type']).click()
        admin_browser.find_by_text('English').click()
        admin_browser.fill('title_en', child_page['title'])
        admin_browser.find_by_text('Promote').click()
        admin_browser.fill('slug_en', slugify(child_page['title']))
        admin_browser.find_by_xpath('//*[@class="dropdown-toggle icon icon-arrow-up"]').click()
        admin_browser.find_by_text('Publish').click()
        assert admin_browser.find_by_text(child_page['title'])
