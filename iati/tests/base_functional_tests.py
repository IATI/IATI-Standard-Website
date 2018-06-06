"""A module of functional tests for base site functionality."""
import os
import string
import random
import time
import pytest
from conftest import LOCALHOST
from django.core.management import call_command
from django.apps import apps
# from django.utils.text import slugify
from django.conf import settings
# from home.models import AbstractContentPage, IATIStreamBlock, HomePage
from wagtail.core.blocks import CharBlock, FieldBlock, RawHTMLBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


TEST_DATA_DIR = settings.BASE_DIR + '/tests/data/'


def prevent_alerts(admin_browser):
    """Stop the Wagtail CMS from sending beforeunload alerts.

    Args:
        admin_browser (browser): The splinter browser instance.

    """
    admin_browser.driver.execute_script("window.removeEventListener('beforeunload', window.areYouSure);")


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


def wait_for_visibility(element, wait_time=1):
    """Wait until an element is visible before scrolling.

    Args:
        element (ElementAPI): The splinter element to be waited on.
        wait_time (int): The time in seconds to wait.

    """
    end_time = time.time() + wait_time

    while time.time() < end_time:
        if element and element.visible:
            return True
    return False


def collect_base_pages(base_page_class):
    """Given an base page class, return models belonging to that app that inherit from the base page class.

    Args:
        base_page_class (Page): The abstract page model to filter all app models by.

    """
    models = list()
    for model in apps.get_models():
        if issubclass(model, base_page_class):
            models.append(model)
    return models


def random_string(size=10, chars=string.ascii_uppercase + string.ascii_lowercase):
    """Return a random string for testing fields.

    Args:
        size (int): Length of desired string.
        chars (list): List of allowable characters in the desired string.

    """
    return ''.join(random.choice(chars) for _ in range(size))


def click_obscured(admin_browser, element):
    """A function that clicks elements even if they're slightly obscured.

    Args:
        admin_browser (browser): The splinter browser instance.
        element (ElementAPI): The splinter element to be waited on.

    """
    wait_for_clickability(element)
    admin_browser.driver.execute_script("arguments[0].click();", element.__dict__['_element'])


def scroll_to_element(admin_browser, element):
    """A function that scrolls to the location of an element.

    Args:
        admin_browser (browser): The splinter browser instance.
        element (ElementAPI): The splinter element to be waited on.

    """
    wait_for_visibility(element)
    rect = admin_browser.driver.execute_script("return arguments[0].getBoundingClientRect();", element.__dict__['_element'])
    mid_point_x = int(rect['x'] + (rect['width'] / 2))
    end_point_y = int(rect['y'] + (rect['height']))
    admin_browser.driver.execute_script("window.scrollTo({}, {});".format(mid_point_x, end_point_y))


def scroll_and_click(admin_browser, element):
    """A function that scrolls to, and clicks an element.

    Args:
        admin_browser (browser): The splinter browser instance.
        element (ElementAPI): The splinter element to be waited on.

    """
    scroll_to_element(admin_browser, element)
    click_obscured(admin_browser, element)


def find_and_click_add_button(admin_browser, base_block):
    """Find a content editor add field button and click it.

    Args:
        admin_browser (browser): The splinter browser instance.
        base_block (str): The name of the block to be added.

    """
    add_button_class = ".action-add-block-{}".format(base_block)
    add_button = admin_browser.find_by_css(add_button_class)[0]
    scroll_and_click(admin_browser, add_button)


def find_and_click_toggle_button(admin_browser, toggle_index):
    """Find a content editor add block button and click it.

    Args:
        admin_browser (browser): The splinter browser instance.
        toggle_index (int): The zero-based index to select the toggle button.

    """
    toggle_button = admin_browser.find_by_css(".toggle")[toggle_index]
    scroll_and_click(admin_browser, toggle_button)


def fill_content_editor_block(admin_browser, base_block, text_field_class, content):
    """Find a content editor text field by class name and fill it.

    Args:
        admin_browser (browser): The splinter browser instance.
        base_block (str): The name of the block to be added.
        text_field_cass (str): The additional CSS selector needed to find the input field.
        content (str): The content to fill the input.

    """
    full_text_field_class = ".fieldname-{}".format(base_block) + text_field_class
    text_field = admin_browser.find_by_css(full_text_field_class)[0]
    scroll_and_click(admin_browser, text_field)
    if text_field.tag_name in ["input", "textarea"]:
        admin_browser.driver.execute_script("arguments[0].value = '{}';".format(content), text_field.__dict__['_element'])
    else:
        text_field.fill(content)


@pytest.mark.django_db()
class TestCreateDefaultPagesManagementCommand():
    """A container for tests that check createdefaultpages command."""

    def test_create_default_pages_idempotence(self, browser):
        """Check pages have URLs after running command a second time after initial setup."""
        browser.visit(os.environ["LIVE_SERVER_URL"])
        browser.click_link_by_text("About")
        valid_url = browser.url
        call_command("createdefaultpages")
        browser.visit(os.environ["LIVE_SERVER_URL"])
        browser.click_link_by_text("About")
        assert browser.url == valid_url


class TestDefaultPages():
    """A container for tests that the default pages exist."""

    DEFAULT_PAGES = [
        {'name': 'Home', 'slug': ''},
        {'name': 'About', 'slug': 'about'},
        {'name': 'Contact', 'slug': 'contact'},
        {'name': 'Events', 'slug': 'events'},
        {'name': 'News', 'slug': 'news'},
        {'name': 'Guidance and Support', 'slug': 'guidance_and_support'}
    ]

    def navigate_to_edit_home_page(self, admin_browser, default_page_name):
        """Navigate to the editable section of the CMS for the Home Page."""
        admin_browser.click_link_by_text('Pages')
        admin_browser.find_by_text('Home').click()
        admin_browser.click_link_by_text(default_page_name)

    def upload_an_image(self, admin_browser):
        """Upload an image in the CMS."""
        admin_browser.driver.set_speed(5)
        admin_browser.find_by_text('Choose an image').click()
        click_obscured(admin_browser, admin_browser.find_by_text('Upload').first)
        admin_browser.fill('title', 'Test image')
        admin_browser.attach_file('file', TEST_DATA_DIR + 'pigeons.jpeg')
        admin_browser.find_by_xpath('//em[contains(text(), "Upload")]').click()
        admin_browser.driver.set_speed(0)

    def publish_changes(self, admin_browser):
        """Publish changes made in the CMS to the live page."""
        click_obscured(admin_browser, admin_browser.find_by_xpath('//div[@class="dropdown-toggle icon icon-arrow-up"]').first)
        click_obscured(admin_browser, admin_browser.find_by_text('Publish').first)

    def view_live_page(self, admin_browser):
        """Visit the url of the 'View live' button so tests don't open a new window"""
        top_view_live_button = admin_browser.find_by_text('View live').first
        page_url = top_view_live_button._element.get_property('href')
        admin_browser.visit(page_url)

    @pytest.mark.parametrize("page_name", DEFAULT_PAGES)
    def test_default_pages_exist(self, browser, page_name):
        """Check default pages exist."""
        browser.visit(LOCALHOST + '{}'.format(page_name['slug']))
        if page_name['slug'] == '':
            page_title = 'Home'
        else:
            page_title = page_name['slug'].replace('_', ' ').capitalize()
        assert browser.title == page_title

    @pytest.mark.parametrize('default_page', DEFAULT_PAGES)
    @pytest.mark.django_db
    def test_header_image_is_editable(self, admin_browser, default_page):
        """Check that the header image for the Home page can be edited in the CMS."""
        self.navigate_to_edit_home_page(admin_browser, default_page['name'])
        admin_browser.find_by_text('Multilingual').click()
        self.upload_an_image(admin_browser)
        self.publish_changes(admin_browser)
        self.view_live_page(admin_browser)
        assert admin_browser.is_element_present_by_xpath('//img[@alt="Test image"]')


class TestTopMenu():
    """A container for tests that the top menu navigation works."""

    @pytest.mark.parametrize('main_section', [
        'about',
        'contact',
        'events',
        'news',
        'support'
    ])
    def test_top_menu(self, browser, main_section):
        """Check links to default site pages in the top menu navigate to the expected page."""
        browser.visit(LOCALHOST)
        browser.click_link_by_id('section-{}'.format(main_section))
        assert browser.find_by_css('body').first.has_class('body--{}'.format(main_section))


class StreamFieldFiller():
    """A class for autofilling streamfield blocks."""

    def __init__(self, admin_browser, stream_block_model):
        """Initialize the class.

        Args:
            admin_browser (browser): The splinter browser instance.
            stream_block_model (StreamBlock): The model for the streamblock to be filled.

        """
        self.random_content = list()
        self.admin_browser = admin_browser
        self.stream_block_model = stream_block_model
        self.possible_ancestors = [
            (CharBlock, self.fill_charblock),
            (TextBlock, self.fill_textblock),
            (RawHTMLBlock, self.fill_textblock),
            (RichTextBlock, self.fill_richtextblock),
            (DocumentChooserBlock, self.fill_documentchooserblock),
            (ImageChooserBlock, self.fill_imagechooserblock),
            (StructBlock, self.fill_structblock),
            (StreamBlock, self.fill_streamblock),
            (FieldBlock, self.pass_block),
        ]

    def find_filler(self, block_model):
        """Given the list of possible ancestors above, find the match and return the appropriate filler function.

        Args:
            block_model (FieldBlock): Base wagtail block of the field to fill.

        """
        for (possible_ancestor, filler_function) in self.possible_ancestors:
            if isinstance(block_model, possible_ancestor):
                return filler_function

    def model_router(self, parent_model_blocks, base_block, depth=0):
        """Route a block to a filler function.

        Args:
            parent_model_blocks (list): List of all sibling blocks.
            base_block (str): Name of the block being filled.
            depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.

        """
        block_model = parent_model_blocks[base_block]
        filler_function = self.find_filler(block_model)
        filler_function(parent_model_blocks, base_block, depth)

    def start_filling(self):
        """Iterate through first layer of child models and start filling them."""
        for base_block in self.stream_block_model.base_blocks:
            self.model_router(self.stream_block_model.base_blocks, base_block)

    def gen_rs(self):
        """Generate a random string and append it to the list to test the live page against."""
        the_string = random_string()
        self.random_content.append(the_string)
        return the_string

    def pass_block(self, _, base_block, depth):
        """Ignore a block. Used for drop-down choices with default settings.

        Args:
            base_block (str): Name of the block being filled.
            depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.

        """
        if depth >= 0:
            find_and_click_add_button(self.admin_browser, base_block)
            find_and_click_toggle_button(self.admin_browser, depth)

    def fill_charblock(self, _, base_block, depth):
        """Fill a character block.

        Args:
            base_block (str): Name of the block being filled.
            depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.

        """
        if depth >= 0:
            find_and_click_add_button(self.admin_browser, base_block)
            find_and_click_toggle_button(self.admin_browser, depth)
        fill_content_editor_block(self.admin_browser, base_block, " input", self.gen_rs())

    def fill_textblock(self, _, base_block, depth):
        """Fill a text block.

        Args:
            base_block (str): Name of the block being filled.
            depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.

        """
        if depth >= 0:
            find_and_click_add_button(self.admin_browser, base_block)
            find_and_click_toggle_button(self.admin_browser, depth)
        fill_content_editor_block(self.admin_browser, base_block, " textarea", self.gen_rs())

    def fill_richtextblock(self, _, base_block, depth):
        """Fill a richtext block.

        Args:
            base_block (str): Name of the block being filled.
            depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.

        """
        if depth >= 0:
            find_and_click_add_button(self.admin_browser, base_block)
            find_and_click_toggle_button(self.admin_browser, depth)
        fill_content_editor_block(self.admin_browser, base_block, " .public-DraftEditor-content", self.gen_rs())

    def fill_documentchooserblock(self, _, base_block, depth):
        """Fill a document block.

        Args:
            base_block (str): Name of the block being filled.
            depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.

        """
        if depth >= 0:
            find_and_click_add_button(self.admin_browser, base_block)
            find_and_click_toggle_button(self.admin_browser, depth)
        choose_doc_button = self.admin_browser.find_by_text("Choose a document")[0]
        scroll_and_click(self.admin_browser, choose_doc_button)
        doc_title = "Annual report"
        self.random_content.append(doc_title)
        annual_report_link = self.admin_browser.find_by_text(doc_title)
        if annual_report_link:
            scroll_and_click(self.admin_browser, annual_report_link[0])
        else:
            upload_tab, upload_button = self.admin_browser.find_by_text('Upload')
            scroll_and_click(self.admin_browser, upload_tab)
            title_field = self.admin_browser.find_by_xpath("//input[@name='title']")[0]
            scroll_and_click(self.admin_browser, title_field)
            title_field.fill(doc_title)
            self.admin_browser.attach_file('file', settings.BASE_DIR + "/tests/data/annual-report.pdf")
            scroll_and_click(self.admin_browser, upload_button)
            self.admin_browser.is_element_not_present_by_text("Upload", wait_time=1)

    def fill_imagechooserblock(self, _, base_block, depth):
        """Fill an image block.

        Args:
            base_block (str): Name of the block being filled.
            depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.

        """
        if depth >= 0:
            find_and_click_add_button(self.admin_browser, base_block)
            find_and_click_toggle_button(self.admin_browser, depth)
        choose_image_button = self.admin_browser.find_by_text("Choose an image")[0]
        scroll_and_click(self.admin_browser, choose_image_button)
        image_title = "Placeholder image"
        image_link = self.admin_browser.find_by_text(image_title)
        if image_link:
            scroll_and_click(self.admin_browser, image_link[0])
        else:
            upload_tab, upload_button = self.admin_browser.find_by_text('Upload')
            scroll_and_click(self.admin_browser, upload_tab)
            title_field = self.admin_browser.find_by_xpath("//input[@name='title']")[0]
            scroll_and_click(self.admin_browser, title_field)
            title_field.fill(image_title)
            self.admin_browser.attach_file('file', settings.BASE_DIR + "/tests/data/placeholder.jpg")
            scroll_and_click(self.admin_browser, upload_button)
            self.admin_browser.is_element_not_present_by_text("Upload", wait_time=1)

    def fill_streamblock(self, parent_model_blocks, base_block, depth):
        """Route a block to a filler function.

        Args:
            parent_model_blocks (list): List of all sibling blocks.
            base_block (str): Name of the block being filled.
            depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.

        """
        find_and_click_add_button(self.admin_browser, base_block)
        block_model = parent_model_blocks[base_block]
        child_blocks = block_model.child_blocks
        depth_1 = depth + 1
        for child_block in child_blocks:
            self.model_router(child_blocks, child_block, depth_1)
        find_and_click_toggle_button(self.admin_browser, depth)

    def fill_structblock(self, parent_model_blocks, base_block, depth):
        """Route a block to a filler function.

        Args:
            parent_model_blocks (list): List of all sibling blocks.
            base_block (str): Name of the block being filled.
            depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.

        """
        find_and_click_add_button(self.admin_browser, base_block)
        block_model = parent_model_blocks[base_block]
        child_blocks = block_model.child_blocks
        for child_block in child_blocks:
            self.model_router(child_blocks, child_block, -1)
        find_and_click_toggle_button(self.admin_browser, depth)


# @pytest.mark.django_db()
# class TestContentEditor():
#     """A container for testing models that incorporate the default content editor.
#     TODO:
#         Tests currently failing in a complex way on Travis.
#         Cannot fix these issues within the current scope so work on this test class has been postponed.
#
#     """
#
#     @pytest.mark.parametrize('content_model', collect_base_pages(AbstractContentPage))
#     def test_content_pages(self, admin_browser, content_model):
#         """
#         Test templates for every content page.
#         Fill in random content for every field and test to see if it exists on the template.
#         """
#         homepage = HomePage.objects.first()
#         admin_browser.visit(os.environ["LIVE_SERVER_URL"]+'/admin/pages/{}/'.format(homepage.pk))
#         admin_browser.click_link_by_text('Add child page')
#         verbose_page_name = content_model.get_verbose_name()
#         if content_model.can_create_at(homepage):
#             admin_browser.click_link_by_text(verbose_page_name)
#             prevent_alerts(admin_browser)
#             admin_browser.find_by_text('English').click()
#             admin_browser.fill('title_en', verbose_page_name)
#             content_editor_filler = StreamFieldFiller(admin_browser, IATIStreamBlock)
#             content_editor_filler.start_filling()
#             promote_tab = admin_browser.find_by_text('Promote')[0]
#             scroll_and_click(admin_browser, promote_tab)
#             admin_browser.fill('slug_en', slugify(verbose_page_name))
#             publish_arrow = admin_browser.find_by_xpath('//div[@class="dropdown-toggle icon icon-arrow-up"]')[0]
#             scroll_and_click(admin_browser, publish_arrow)
#             publish_button = admin_browser.find_by_text('Publish')[0]
#             scroll_and_click(admin_browser, publish_button)
#             button_link = admin_browser.find_by_css('li.success a')[0]
#             href = button_link.__dict__['_element'].get_property('href')
#             admin_browser.visit(href)
#             for random_content in content_editor_filler.random_content:
#                 assert admin_browser.is_text_present(random_content)
