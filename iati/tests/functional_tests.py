"""A module for functional tests."""
import pytest
from conftest import LOCALHOST


class TestHomePageExists():
    """A container for tests that the home page exists."""

    def setup_home_page_tests(self, browser):
        """Visit the home page and locate the IATI logo."""
        browser.visit(LOCALHOST)
        logo = browser.find_by_css("a.branding").first
        return logo

    def test_home_page_loads(self, browser):
        """Check that the home page loads."""
        self.setup_home_page_tests(browser)
        assert browser.status_code.code == 200

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


class TestTopMenu():
    """A container for tests that the top menu navigation works."""

    @pytest.mark.parametrize("main_section", [
        "about",
        "contact",
        "events",
        "news",
        "support"
    ])
    def test_top_menu(self, browser, main_section):
        """Check links to default site pages in the top menu navigate to the expected page."""
        browser.visit(LOCALHOST)
        browser.click_link_by_id("section-{}".format(main_section))
        assert browser.find_by_css("body").first.has_class("body--{}".format(main_section))


class TestAdminLogin():
    """A container for tests that check admins can login to the CMS."""

    def test_admin_login(self, admin_browser):
        """Login to the admin page and check the Wagtail CMS logo is on the page."""
        wagtail_logo = "//img[@class='wagtail-logo wagtail-logo__body']"
        assert admin_browser.find_by_xpath(wagtail_logo).first.visible
