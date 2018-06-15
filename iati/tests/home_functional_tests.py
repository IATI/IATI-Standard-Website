"""A module of functional tests for the home page."""
import os
import pytest
from django.utils.text import slugify


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
    """Publish page created in the CMS. A duplicate function from about_functional_tests.py."""
    admin_browser.find_by_xpath('//div[@class="dropdown-toggle icon icon-arrow-up"]').click()
    admin_browser.find_by_text('Publish').click()


def create_standard_home_page(admin_browser, page_type, fixed_page_type, page_title):
    """Create a child page in the CMS.

    Args:
        page_type (str): The verbose name of the page model type you want to click on.
        fixed_page_type (str): The value of the fixed page dropdown (e.g. "privacy" for "PrivacyPage")
        page_title (str): The title of the page you are editing.

    """
    admin_browser.visit(os.environ['LIVE_SERVER_URL'] + "/admin/pages/3/")
    admin_browser.find_by_text('Add child page').click()
    admin_browser.find_by_text(page_type).click()
    dropdown = admin_browser.find_by_id("id_fixed_page_type")[0]
    dropdown.select(fixed_page_type)
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


@pytest.mark.django_db
class TestFixedStandardPages():
    """Tests to see if fixed standard pages are properly linked"""
    @pytest.mark.parametrize('fixed_page', [
        PRIVACY_PAGE,
        TERMS_PAGE
    ])
    def test_can_create_standard_pages(self, admin_browser, fixed_page):
        """Check that when an event index child page is created it appears in the website."""
        create_standard_home_page(admin_browser, fixed_page['page_type'], fixed_page['fixed_page_type'], fixed_page['title'])
        view_live_page(admin_browser, fixed_page['title'])
        assert admin_browser.title == fixed_page['title']
        admin_browser.click_link_by_text(fixed_page['base_link_text'])
        assert admin_browser.title == fixed_page['title']
