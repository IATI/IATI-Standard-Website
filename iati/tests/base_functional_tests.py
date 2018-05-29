"""A module of functional tests for base site functionality."""
import os
import pytest
from conftest import LOCALHOST
from django.core.management import call_command
from django.apps import apps
from django.utils.text import slugify
from django.conf import settings
from home.models import AbstractContentPage, IATIStreamBlock, HomePage
from wagtail.core.blocks import CharBlock, FieldBlock, RawHTMLBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
import string
import random
import time


# def prevent_alerts(admin_browser):
#     """Stop the Wagtail CMS from sending alerts"""
#     admin_browser.driver.execute_script("window.removeEventListener('beforeunload', window.areYouSure);")


def wait_for_clickability(element, wait_time=1):
    """Wait until an element is enabled before clicking."""
    end_time = time.time() + wait_time

    while time.time() < end_time:
        if element and element.__dict__['_element'].is_enabled():
            return True
    return False


def wait_for_visibility(element, wait_time=1):
    """Wait until an element is visible before scrolling."""
    end_time = time.time() + wait_time

    while time.time() < end_time:
        if element and element.visible:
            return True
    return False


def collect_base_pages(base_page_class):
    """Given an base page class, return models belonging to that app that inherit from AbstractContentPage"""
    models = list()
    for model in apps.get_models():
        if issubclass(model, base_page_class):
            models.append(model)
    return models


def random_string(size=10, chars=string.ascii_uppercase+string.ascii_lowercase):
    """Return a random string for testing fields."""
    return ''.join(random.choice(chars) for _ in range(size))


def click_obscured(admin_browser, element):
    """A function that clicks elements even if they're slightly obscured."""
    wait_for_clickability(element)
    admin_browser.driver.execute_script("arguments[0].click();", element.__dict__['_element'])


def scroll_to_element(admin_browser, element):
    """A function that scrolls to the location of an element."""
    wait_for_visibility(element)
    rect = admin_browser.driver.execute_script("return arguments[0].getBoundingClientRect();", element.__dict__['_element'])
    mid_point_x = int(rect['x'] + (rect['width']/2))
    end_point_y = int(rect['y'] + (rect['height']))
    admin_browser.driver.execute_script("window.scrollTo({}, {});".format(mid_point_x, end_point_y))


def scroll_and_click(admin_browser, element):
    """A function that scrolls to, and clicks an element."""
    scroll_to_element(admin_browser, element)
    click_obscured(admin_browser, element)


def find_and_click_add_button(admin_browser, base_block):
    """Find a content editor add field button and click it."""
    add_button_class = ".action-add-block-{}".format(base_block)
    add_button = admin_browser.find_by_css(add_button_class)[0]
    scroll_and_click(admin_browser, add_button)


def find_and_click_toggle_button(admin_browser, toggle_index):
    """Find a content editor add block button and click it."""
    toggle_button = admin_browser.find_by_css(".toggle")[toggle_index]
    scroll_and_click(admin_browser, toggle_button)


def fill_content_editor_block(admin_browser, base_block, text_field_class, content):
    """Find a content editor text field by class name and fill it."""
    full_text_field_class = ".fieldname-{}".format(base_block)+text_field_class
    text_field = admin_browser.find_by_css(full_text_field_class)[0]
    scroll_and_click(admin_browser, text_field)
    if text_field.tag_name in ["input", "textarea"]:
        admin_browser.driver.execute_script("arguments[0].value = '{}';".format(content), text_field.__dict__['_element'])
    else:
        text_field.fill(content)


@pytest.mark.django_db()
class TestCreateDefaultPages():
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


class TestDefaultPagesExist():
    """A container for tests that the default pages exist."""

    @pytest.mark.parametrize("page_name", [
        'about',
        'contact',
        'events',
        'news',
        'guidance_and_support'
    ])
    def test_default_pages_exist(self, browser, page_name):
        """Check default pages exist."""
        browser.visit(LOCALHOST + '{}'.format(page_name))
        page_title = page_name.replace('_', ' ').capitalize()
        assert browser.title == page_title


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
    """A class for autofilling streamfield blocks"""

    def __init__(self, admin_browser, stream_block_model):
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
        for (possible_ancestor, filler_function) in self.possible_ancestors:
            if isinstance(block_model, possible_ancestor):
                return filler_function

    def model_router(self, parent_model_blocks, base_block, depth=0):
        block_model = parent_model_blocks[base_block]
        filler_function = self.find_filler(block_model)
        filler_function(parent_model_blocks, base_block, depth)

    def start_filling(self):
        for base_block in self.stream_block_model.base_blocks:
            self.model_router(self.stream_block_model.base_blocks, base_block)

    def gen_rs(self):
        the_string = random_string()
        self.random_content.append(the_string)
        return the_string

    def pass_block(self, _, base_block, depth):
        if depth >= 0:
            find_and_click_add_button(self.admin_browser, base_block)
            find_and_click_toggle_button(self.admin_browser, depth)

    def fill_charblock(self, _, base_block, depth):
        if depth >= 0:
            find_and_click_add_button(self.admin_browser, base_block)
            find_and_click_toggle_button(self.admin_browser, depth)
        fill_content_editor_block(self.admin_browser, base_block, " input", self.gen_rs())

    def fill_textblock(self, _, base_block, depth):
        if depth >= 0:
            find_and_click_add_button(self.admin_browser, base_block)
            find_and_click_toggle_button(self.admin_browser, depth)
        fill_content_editor_block(self.admin_browser, base_block, " textarea", self.gen_rs())

    def fill_richtextblock(self, _, base_block, depth):
        if depth >= 0:
            find_and_click_add_button(self.admin_browser, base_block)
            find_and_click_toggle_button(self.admin_browser, depth)
        fill_content_editor_block(self.admin_browser, base_block, " .public-DraftEditor-content", self.gen_rs())

    def fill_documentchooserblock(self, _, base_block, depth):
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
            self.admin_browser.attach_file('file', settings.BASE_DIR+"/tests/data/annual-report.pdf")
            scroll_and_click(self.admin_browser, upload_button)
            self.admin_browser.is_element_not_present_by_text("Upload", wait_time=1)

    def fill_imagechooserblock(self, _, base_block, depth):
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
            self.admin_browser.attach_file('file', settings.BASE_DIR+"/tests/data/placeholder.jpg")
            scroll_and_click(self.admin_browser, upload_button)
            self.admin_browser.is_element_not_present_by_text("Upload", wait_time=1)

    def fill_streamblock(self, parent_model_blocks, base_block, depth):
        find_and_click_add_button(self.admin_browser, base_block)
        block_model = parent_model_blocks[base_block]
        child_blocks = block_model.child_blocks
        depth_1 = depth + 1
        for child_block in child_blocks:
            self.model_router(child_blocks, child_block, depth_1)
        find_and_click_toggle_button(self.admin_browser, depth)

    def fill_structblock(self, parent_model_blocks, base_block, depth):
        find_and_click_add_button(self.admin_browser, base_block)
        block_model = parent_model_blocks[base_block]
        child_blocks = block_model.child_blocks
        for child_block in child_blocks:
            self.model_router(child_blocks, child_block, -1)
        find_and_click_toggle_button(self.admin_browser, depth)

H2 = {'content': 'H2 heading', 'button': 'H2', 'id': 'content_editor_en-{}-value'}
H3 = {'content': 'H3 heading', 'button': 'H3', 'id': 'content_editor_en-{}-value'}
H4 = {'content': 'H4 heading', 'button': 'H4', 'id': 'content_editor_en-{}-value'}

def navigate_to_default_page_cms_section(admin_browser, default_page_title):
    """Navigate to the About page section of the CMS.

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


def publish_page(admin_browser):
    """Publish page created in the CMS."""
    admin_browser.find_by_xpath('//div[@class="dropdown-toggle icon icon-arrow-up"]').click()
    admin_browser.find_by_text('Publish').click()


def create_about_child_page(admin_browser, page_type, page_title):
    """Create a child page in the CMS.

    Args:
        page_type (str): The verbose name of the page model type you want to click on.
        page_title (str): The title of the page you are editing.

    """
    navigate_to_default_page_cms_section(admin_browser, 'About')
    admin_browser.find_by_text('Add child page').click()
    admin_browser.find_by_text(page_type).click()
    enter_page_content(admin_browser, 'English', 'title_en', page_title)
    enter_page_content(admin_browser, 'Promote', 'slug_en', slugify(page_title))
    publish_page(admin_browser)


def view_live_page(admin_browser, page_title):
    """Navigate to the published page on the site.

    Args:
        page_title (str): The page title text you are expecting on the live page.

    """
    admin_browser.find_by_text(page_title).mouse_over()
    button_link = admin_browser.find_by_text('View live')
    href = button_link[0].__dict__['_element'].get_property('href')
    admin_browser.visit(href)


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
    if not admin_browser.find_by_text(button).visible:
        admin_browser.find_by_xpath('//div[@id="content_editor_en-{}-appendmenu"]/a'.format(int(element_count)-1)).mouse_over()
        admin_browser.find_by_xpath('//div[@id="content_editor_en-{}-appendmenu"]/a'.format(int(element_count)-1)).click()
        scroll_to_bottom_of_page(admin_browser)


@pytest.mark.django_db()
class TestContentPages():
    """A container for testing models that incorporate the default content editor"""

    # @pytest.mark.parametrize('header', [
    #     H2,
    #     H3,
    #     H4
    # ])
    @pytest.mark.parametrize('content_model', collect_base_pages(AbstractContentPage))
    def test_content_editor_adds_headers(self, admin_browser, content_model):
        """
        Test templates for every content page.
        Fill in random content for every field and test to see if it exists on the template.
        """
        homepage = HomePage.objects.first()
        admin_browser.visit(os.environ["LIVE_SERVER_URL"] + '/admin/pages/{}/'.format(homepage.pk))
        admin_browser.click_link_by_text('Add child page')
        verbose_page_name = content_model.get_verbose_name()
        if content_model.can_create_at(homepage):
            admin_browser.click_link_by_text(verbose_page_name)
            # prevent_alerts(admin_browser)
            admin_browser.find_by_text('English').click()
            admin_browser.fill('title_en', verbose_page_name)
            scroll_to_bottom_of_page(admin_browser)
            element_count = admin_browser.find_by_id('content_editor_en-count').value
            reveal_content_editor(admin_browser, H3['button'], element_count)
            admin_browser.find_by_text(H3['button'])[int(element_count)].click()
            admin_browser.find_by_id(H3['id'].format(element_count)).fill(H3['content'])
            publish_page(admin_browser)
            view_live_page(admin_browser, verbose_page_name)
            assert admin_browser.is_text_present(H3['content'])
            # content_editor_filler = StreamFieldFiller(admin_browser, IATIStreamBlock)
            # content_editor_filler.start_filling()
            # promote_tab = admin_browser.find_by_text('Promote')[0]
            # scroll_and_click(admin_browser, promote_tab)
            # admin_browser.fill('slug_en', slugify(verbose_page_name))
            # publish_arrow = admin_browser.find_by_xpath('//div[@class="dropdown-toggle icon icon-arrow-up"]')[0]
            # scroll_and_click(admin_browser, publish_arrow)
            # publish_button = admin_browser.find_by_text('Publish')[0]
            # scroll_and_click(admin_browser, publish_button)
            # button_link = admin_browser.find_by_css('li.success a')[0]
            # href = button_link.__dict__['_element'].get_property('href')
            # admin_browser.visit(href)
            # for random_content in content_editor_filler.random_content:
            #     assert admin_browser.is_text_present(random_content)
