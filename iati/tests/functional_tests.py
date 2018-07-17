"""A module for functional tests."""
from conftest import LOCALHOST


class TestHomePageExists():
    """A container for tests that the home page exists."""

    def setup_home_page_tests(self, browser):
        """Visit the home page and locate the IATI logo."""
        browser.visit(LOCALHOST)
        logo = browser.find_by_css('a.branding').first
        return logo

    def test_home_page_has_IATI_logo(self, browser):
        """Check the IATI logo appears on the page."""
        logo = self.setup_home_page_tests(browser)
        assert logo.visible

    def test_home_page_logo_is_a_home_link(self, browser):
        """Check that the IATI logo is also a link to the home page."""
        logo = self.setup_home_page_tests(browser)
        past_url = browser.url
        logo.click()
        assert past_url == browser.url
