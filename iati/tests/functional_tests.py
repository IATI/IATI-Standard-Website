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
    assert browser.url == localhost + 'en/'
    assert browser.title == 'Home'
    browser.quit()

# def test_about_page_exists(browser):
#     """A test to check for the parent about page."""
#     browser.visit(localhost)
#     button = browser.find_by_name()
