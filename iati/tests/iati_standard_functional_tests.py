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
    admin_browser.find_by_text('English')[0].click()
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
        admin_browser.find_by_text('English')[0].click()
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
        admin_browser.find_by_text('English')[0].click()
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
        admin_browser.find_by_text('English')[0].click()
        element_count = admin_browser.find_by_id('content_editor_en-count').value
        scroll_to_bottom_of_page(admin_browser)
        reveal_content_editor(admin_browser, 'Intro', element_count)
        admin_browser.find_by_text('Intro')[int(element_count)].click()
        admin_browser.find_by_xpath('//div[@class="notranslate public-DraftEditor-content"]').fill('This is some content.')
        publish_changes(admin_browser)
        view_live_page(admin_browser)
        assert admin_browser.is_text_present('This is some content.')


# I want to be directed to the appropriate section of the old IATI standard site for me
@pytest.mark.django_db
class TestRedirectLinksWorking():
    """Container for tests that check redirects are correct and working."""

    LOCALHOST_LINK = str()

    def visit_iati_standard_page(self, admin_browser):
        """Go to the IATI Stadard page from the admin site."""
        page_button = admin_browser.find_by_xpath('//a[@href="/en/iati-standard/"]').first
        page_link = page_button._element.get_property('href')
        self.LOCALHOST_LINK = page_link[:-15]
        admin_browser.visit(page_link)

    ORG_STANDARD = {'id': 'org-standard', 'expected_content': 'This section details the IATI Organisation standard.'}
    ACTIVITY_STANDARD = {'id': 'act-standard', 'expected_content': 'This section details the IATI Activity standard.'}
    CODELISTS = {'id': 'codelists', 'expected_content': 'The IATI codelists are key to making IATI activity and organisation data from different publishers comparable.'}
    SCHEMA = {'id': 'schema', 'expected_content': 'The IATI standard consists of a number of schema,'}
    ORG_IDS = {'id': 'org-ids', 'expected_content': 'Organisational identifiers have two uses in IATI.'}
    STANDARD_UPGRADE = {'id': 'standard-upgrade', 'expected_content': 'The IATI standard is a living entity that will require improvement over time.'}
    PREV_VERSIONS = {'id': 'prev-versions', 'expected_content': 'Links to all versions IATI Standard documentation are available below.'}
    VER_202 = {'id': '202', 'expected_content': 'This is version 2.02 of the IATI Standard.'}
    VER_201 = {'id': '201', 'expected_content': 'This is version 2.01 of the IATI Standard.'}
    VER_105 = {'id': '105', 'expected_content': 'This is version 1.05 of the IATI Standard.'}
    INFO_FOR_DEVS = {'id': 'info-for-devs', 'expected_content': 'This section contains various pieces documentation targetted at developers'}
    DATASTORE_GUIDE = {'id': 'datastore-guide', 'expected_content': 'The Datastore stores all activity data available on the IATI Registry,'}

    HARDCODED_LINKS = [ORG_STANDARD, ACTIVITY_STANDARD, CODELISTS, SCHEMA, ORG_IDS, STANDARD_UPGRADE, PREV_VERSIONS, VER_202, VER_201, VER_105, INFO_FOR_DEVS, DATASTORE_GUIDE]

    @pytest.mark.parametrize('link', HARDCODED_LINKS)
    def test_hardcoded_links_work(self, admin_browser, link):
        """Check that the given link goes to the correct page.

        Note:
            The weird browser visit after the test assertion is due to a login error occuring during parametrization that wasn't logging out of the admin site and then logging in fresh for the next parametrized test.

        """
        self.visit_iati_standard_page(admin_browser)
        admin_browser.find_by_id(link['id']).click()
        assert admin_browser.is_text_present(link['expected_content'])
        admin_browser.visit(self.LOCALHOST_LINK)
