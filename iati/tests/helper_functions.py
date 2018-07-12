import time
from django.utils.text import slugify
from tests.about_functional_tests import TEST_DATA_DIR


# helpers from base_functional_tests.py
def wait_for_clickability(element, wait_time=1):
    """Wait until an element is enabled before clicking.

    Args:
        element (ElementAPI): The splinter element to be waited on.
        wait_time (int): The time in seconds to wait.

    """
    end_time = time.time() + wait_time

    while time.time() < end_time:
        if element and element.__dict__['_element'].is_enabled():
            return True
    return False


def click_obscured(admin_browser, element):
    """A function that clicks elements even if they're slightly obscured.

    Args:
        admin_browser (browser): The splinter browser instance.
        element (ElementAPI): The splinter element to be waited on.

    """
    wait_for_clickability(element)
    admin_browser.driver.execute_script("arguments[0].click();", element.__dict__['_element'])


def view_live_page(admin_browser, page_title):
    """Navigate to the published page on the site.

    Args:
        page_title (str): The page title text you are expecting on the live page.

    """
    button_links = admin_browser.find_by_xpath('//a[@title="View live version of \'{}\'"]'.format(page_title))
    href = button_links[0].__dict__['_element'].get_property('href')
    admin_browser.visit(href)


def prevent_alerts(admin_browser):
    """Stop the Wagtail CMS from sending beforeunload alerts.

    Args:
        admin_browser (browser): The splinter browser instance.

    """
    admin_browser.driver.execute_script("window.removeEventListener('beforeunload', window.areYouSure);")


# helpers for iati_standard_functional_tests.py
def navigate_to_Home_cms_section(admin_browser):
    """Navigate to the Home section of the CMS."""
    admin_browser.click_link_by_text('Pages')
    admin_browser.find_by_text('Home').click()


def upload_an_image(admin_browser):
    """Upload an image in the CMS.

    Note:
        Duplicate of the same helper function in base_functional_tests.

    """
    admin_browser.find_by_text('Choose an image').click()
    click_obscured(admin_browser, admin_browser.find_by_text('Upload').first)
    admin_browser.fill('title', 'Test image')
    admin_browser.attach_file('file', TEST_DATA_DIR + 'pigeons.jpeg')
    admin_browser.find_by_xpath('//em[contains(text(), "Upload")]').click()


def publish_changes(admin_browser):
    """Publish changes made in the CMS to the live page."""
    click_obscured(admin_browser, admin_browser.find_by_xpath('//div[@class="dropdown-toggle icon icon-arrow-up"]').first)
    click_obscured(admin_browser, admin_browser.find_by_text('Publish').first)


# helpers for using_data_functional_tests.py
def navigate_to_default_page_cms_section(admin_browser, default_page_title):
    """Navigate to the Using data page section of the CMS.

    Args:
        default_page_title (str): The title of a default page modelself.

    """
    admin_browser.click_link_by_text('Pages')
    admin_browser.find_by_xpath('//span[@class="icon icon-arrow-right "]').click()
    admin_browser.find_by_text(default_page_title).click()


def enter_page_content(admin_browser, tab_name, cms_field, cms_content):
    """Add title and slug to a page in the CMS.

    Args:
        tab_name (str): The name of a tab on an edit page of the CMS.
        cms_field (str): The name of the field in the CMS you want to fill.
        cms_content (str): The text content you want to fill the field with.

    """
    admin_browser.find_by_text(tab_name).click()
    admin_browser.fill(cms_field, cms_content)


def create_using_data_child_page(admin_browser, page_type, page_title):
    """Create a child page in the CMS.

    Args:
        page_type (str): The verbose name of the page model type you want to click on.
        page_title (str): The title of the page you are editing.

    """
    navigate_to_default_page_cms_section(admin_browser, 'Using IATI data')
    admin_browser.find_by_text('Add child page').click()
    admin_browser.find_by_text(page_type).click()
    enter_page_content(admin_browser, 'English', 'title_en', page_title)
    enter_page_content(admin_browser, 'Promote', 'slug_en', slugify(page_title))
    publish_page(admin_browser)


def edit_page_header(admin_browser, page_title, cms_field, cms_content):
    """Edit a page by adding content via the CMS.

    Args:
        page_title (str): The title of the page you want to edit.
        cms_field (str): The name of the CMS field you want to enter content into.
        cms_content (str): The text content you want to add to the CMS field.

    TODO:
        Rename this function to avoid confusion with content editor tests.

    """
    admin_browser.find_by_text(page_title).click()
    enter_page_content(admin_browser, 'English', cms_field, cms_content)
    publish_page(admin_browser)
    view_live_page(admin_browser, page_title)


def publish_page(admin_browser):
    """Publish page created in the CMS.

    Note:
        Duplicate of publish_changes in base_functional_tests.

    """
    click_obscured(admin_browser, admin_browser.find_by_xpath('//div[@class="dropdown-toggle icon icon-arrow-up"]').first)
    click_obscured(admin_browser, admin_browser.find_by_text('Publish').first)


# helpers for news_functional_tests.py
def scroll_to_bottom_of_page(admin_browser):
    """Scroll to the bottom of a page."""
    admin_browser.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def reveal_content_editor(admin_browser, button, element_count):
    """Open content editor if it is not already in view.

    Args:
        button (str): The displayed text name of the button you want to click.
        element_count (str): The element counter value of the content editor Streamfield block.

    TODO:
        Decide whether on convert element_count to int on assignment of variable.

    """
    if not admin_browser.find_by_text(button).visible and int(element_count) > 0:
        toggle = admin_browser.find_by_xpath('//div[@id="content_editor_en-{}-appendmenu"]/a'.format(int(element_count) - 1))[0]
        admin_browser.driver.execute_script("arguments[0].click();", toggle.__dict__['_element'])
        scroll_to_bottom_of_page(admin_browser)


def create_news_child_page(admin_browser, page_type, page_title):
    """Create a child page in the CMS.

    Args:
        page_type (str): The verbose name of the page model type you want to click on.
        page_title (str): The title of the page you are editing.

    """
    navigate_to_default_page_cms_section(admin_browser, 'News')
    admin_browser.find_by_text('Add child page').click()
    admin_browser.find_by_text(page_type).click()
    enter_page_content(admin_browser, 'English', 'title_en', page_title)
    enter_page_content(admin_browser, 'Promote', 'slug_en', slugify(page_title))
    publish_page(admin_browser)
