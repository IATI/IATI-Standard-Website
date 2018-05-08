"""A module of functional tests for the about page and its sub pages."""
# import pytest


# @pytest.mark.django_db()
def test_can_create_about_sub_page(admin_browser):
    """Check that an about sub page can be created for the About page."""
    admin_browser.click_link_by_text('Pages')
    admin_browser.find_by_text('See children').click()
    admin_browser.find_by_text('About').click()
    admin_browser.find_by_text('Add child page').click()
    admin_browser.find_by_text('About sub page').click()
    admin_browser.find_by_text('English').click()
    admin_browser.fill('title_en', 'test sub page')
    admin_browser.find_by_xpath('//*[@class="dropdown-toggle icon icon-arrow-up"]').click()
    admin_browser.find_by_text('Publish').click()
    assert admin_browser.find_by_text('test sub page')
