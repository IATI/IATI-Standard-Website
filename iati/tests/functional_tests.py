# import pytest


localhost = 'http://127.0.0.1:8000/'
# def test_multiple_browsers(browser):
#     """A test to test you can test with multiple browsers at once."""
#     browser.visit('https://www.google.com')
#     assert browser.url == 'https://www.google.com/'
#     browser.quit()

def test_home_page_exists(browser):
    """A test to check for the existence of the home page."""
    browser.visit(localhost)
    # 200 HTTP code
    assert browser.status_code.code == 200
    # Logo is visible
    logo = browser.find_by_css("a.branding").first
    assert logo.visible
    # The link on the logo is the same as the current page
    past_url = browser.url
    logo.click()
    assert past_url == browser.url
    browser.quit()

# def test_about_page_exists(browser):
#     """A test to check for the parent about page."""
#     browser.visit(localhost)
#     button = browser.find_by_name()
