"""A module of functional tests for base site functionality."""
import os
import pytest
from conftest import LOCALHOST
from django.conf import settings
from django.core.management import call_command
# from home.models import AbstractContentPage, IATIStreamBlock, HomePage
from wagtail.core.blocks import CharBlock, FieldBlock, RawHTMLBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from home.management.commands.createdefaultpages import DEFAULT_PAGES
from home.models import HomePage
from tests import helper_functions


DEFAULT_PAGES = DEFAULT_PAGES + [{'title': 'Home', 'slug': '', 'model': HomePage}]


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

    def navigate_to_edit_home_page(self, admin_browser, default_page_name):
        """Navigate to the editable section of the CMS for the Home Page."""
        admin_browser.click_link_by_text('Pages')
        admin_browser.find_by_text('Home').click()

    @pytest.mark.parametrize("page_name", DEFAULT_PAGES)
    def test_default_pages_exist(self, browser, page_name):
        """Check default pages exist."""
        browser.visit(LOCALHOST + '{}'.format(page_name['slug']))
        assert browser.title == page_name['title']

    @pytest.mark.parametrize('default_page', DEFAULT_PAGES)
    @pytest.mark.django_db
    def test_header_image_is_editable(self, admin_browser, default_page):
        """Check that the header image for the Home page can be edited in the CMS."""
        helper_functions.navigate_to_Home_cms_section(admin_browser)
        admin_browser.click_link_by_text(default_page['title'])
        admin_browser.find_by_text('Multilingual').click()
        helper_functions.upload_an_image(admin_browser)
        helper_functions.publish_changes(admin_browser)
        helper_functions.view_live_page(admin_browser, default_page['title'])
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


# class StreamFieldFiller():
#     """A class for autofilling streamfield blocks."""
#
#     def __init__(self, admin_browser, stream_block_model):
#         """Initialize the class.
#
#         Args:
#             admin_browser (browser): The splinter browser instance.
#             stream_block_model (StreamBlock): The model for the streamblock to be filled.
#
#         """
#         self.random_content = list()
#         self.admin_browser = admin_browser
#         self.stream_block_model = stream_block_model
#         self.possible_ancestors = [
#             (CharBlock, self.fill_charblock),
#             (TextBlock, self.fill_textblock),
#             (RawHTMLBlock, self.fill_textblock),
#             (RichTextBlock, self.fill_richtextblock),
#             (DocumentChooserBlock, self.fill_documentchooserblock),
#             (ImageChooserBlock, self.fill_imagechooserblock),
#             (StructBlock, self.fill_structblock),
#             (StreamBlock, self.fill_streamblock),
#             (FieldBlock, self.pass_block),
#         ]
#
#     def find_filler(self, block_model):
#         """Given the list of possible ancestors above, find the match and return the appropriate filler function.
#
#         Args:
#             block_model (FieldBlock): Base wagtail block of the field to fill.
#
#         """
#         for (possible_ancestor, filler_function) in self.possible_ancestors:
#             if isinstance(block_model, possible_ancestor):
#                 return filler_function
#
#     def model_router(self, parent_model_blocks, base_block, depth=0):
#         """Route a block to a filler function.
#
#         Args:
#             parent_model_blocks (list): List of all sibling blocks.
#             base_block (str): Name of the block being filled.
#             depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.
#
#         """
#         block_model = parent_model_blocks[base_block]
#         filler_function = self.find_filler(block_model)
#         filler_function(parent_model_blocks, base_block, depth)
#
#     def start_filling(self):
#         """Iterate through first layer of child models and start filling them."""
#         for base_block in self.stream_block_model.base_blocks:
#             self.model_router(self.stream_block_model.base_blocks, base_block)
#
#     def gen_rs(self):
#         """Generate a random string and append it to the list to test the live page against."""
#         the_string = helper_functions.random_string()
#         self.random_content.append(the_string)
#         return the_string
#
#     def pass_block(self, _, base_block, depth):
#         """Ignore a block. Used for drop-down choices with default settings.
#
#         Args:
#             base_block (str): Name of the block being filled.
#             depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.
#
#         """
#         if depth >= 0:
#             helper_functions.find_and_click_add_button(self.admin_browser, base_block)
#             helper_functions.find_and_click_toggle_button(self.admin_browser, depth)
#
#     def fill_charblock(self, _, base_block, depth):
#         """Fill a character block.
#
#         Args:
#             base_block (str): Name of the block being filled.
#             depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.
#
#         """
#         if depth >= 0:
#             helper_functions.find_and_click_add_button(self.admin_browser, base_block)
#             helper_functions.find_and_click_toggle_button(self.admin_browser, depth)
#         helper_functions.fill_content_editor_block(self.admin_browser, base_block, " input", self.gen_rs())
#
#     def fill_textblock(self, _, base_block, depth):
#         """Fill a text block.
#
#         Args:
#             base_block (str): Name of the block being filled.
#             depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.
#
#         """
#         if depth >= 0:
#             helper_functions.find_and_click_add_button(self.admin_browser, base_block)
#             helper_functions.find_and_click_toggle_button(self.admin_browser, depth)
#         helper_functions.fill_content_editor_block(self.admin_browser, base_block, " textarea", self.gen_rs())
#
#     def fill_richtextblock(self, _, base_block, depth):
#         """Fill a richtext block.
#
#         Args:
#             base_block (str): Name of the block being filled.
#             depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.
#
#         """
#         if depth >= 0:
#             helper_functions.find_and_click_add_button(self.admin_browser, base_block)
#             helper_functions.find_and_click_toggle_button(self.admin_browser, depth)
#         helper_functions.fill_content_editor_block(self.admin_browser, base_block, " .public-DraftEditor-content", self.gen_rs())
#
#     def fill_documentchooserblock(self, _, base_block, depth):
#         """Fill a document block.
#
#         Args:
#             base_block (str): Name of the block being filled.
#             depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.
#
#         """
#         if depth >= 0:
#             helper_functions.find_and_click_add_button(self.admin_browser, base_block)
#             helper_functions.find_and_click_toggle_button(self.admin_browser, depth)
#         choose_doc_button = self.admin_browser.find_by_text("Choose a document")[0]
#         helper_functions.scroll_and_click(self.admin_browser, choose_doc_button)
#         doc_title = "Annual report"
#         self.random_content.append(doc_title)
#         annual_report_link = self.admin_browser.find_by_text(doc_title)
#         if annual_report_link:
#             helper_functions.scroll_and_click(self.admin_browser, annual_report_link[0])
#         else:
#             upload_tab, upload_button = self.admin_browser.find_by_text('Upload')
#             helper_functions.scroll_and_click(self.admin_browser, upload_tab)
#             title_field = self.admin_browser.find_by_xpath("//input[@name='title']")[0]
#             helper_functions.scroll_and_click(self.admin_browser, title_field)
#             title_field.fill(doc_title)
#             self.admin_browser.attach_file('file', settings.BASE_DIR + "/tests/data/annual-report.pdf")
#             helper_functions.scroll_and_click(self.admin_browser, upload_button)
#             self.admin_browser.is_element_not_present_by_text("Upload", wait_time=1)
#
#     def fill_imagechooserblock(self, _, base_block, depth):
#         """Fill an image block.
#
#         Args:
#             base_block (str): Name of the block being filled.
#             depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.
#
#         """
#         if depth >= 0:
#             helper_functions.find_and_click_add_button(self.admin_browser, base_block)
#             helper_functions.find_and_click_toggle_button(self.admin_browser, depth)
#         choose_image_button = self.admin_browser.find_by_text("Choose an image")[0]
#         helper_functions.scroll_and_click(self.admin_browser, choose_image_button)
#         image_title = "Placeholder image"
#         image_link = self.admin_browser.find_by_text(image_title)
#         if image_link:
#             helper_functions.scroll_and_click(self.admin_browser, image_link[0])
#         else:
#             upload_tab, upload_button = self.admin_browser.find_by_text('Upload')
#             helper_functions.scroll_and_click(self.admin_browser, upload_tab)
#             title_field = self.admin_browser.find_by_xpath("//input[@name='title']")[0]
#             helper_functions.scroll_and_click(self.admin_browser, title_field)
#             title_field.fill(image_title)
#             self.admin_browser.attach_file('file', settings.BASE_DIR + "/tests/data/placeholder.jpg")
#             helper_functions.scroll_and_click(self.admin_browser, upload_button)
#             self.admin_browser.is_element_not_present_by_text("Upload", wait_time=1)
#
#     def fill_streamblock(self, parent_model_blocks, base_block, depth):
#         """Route a block to a filler function.
#
#         Args:
#             parent_model_blocks (list): List of all sibling blocks.
#             base_block (str): Name of the block being filled.
#             depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.
#
#         """
#         helper_functions.find_and_click_add_button(self.admin_browser, base_block)
#         block_model = parent_model_blocks[base_block]
#         child_blocks = block_model.child_blocks
#         depth_1 = depth + 1
#         for child_block in child_blocks:
#             self.model_router(child_blocks, child_block, depth_1)
#         helper_functions.find_and_click_toggle_button(self.admin_browser, depth)
#
#     def fill_structblock(self, parent_model_blocks, base_block, depth):
#         """Route a block to a filler function.
#
#         Args:
#             parent_model_blocks (list): List of all sibling blocks.
#             base_block (str): Name of the block being filled.
#             depth (int): For cases where there are nested streamblocks or structblocks, to change adding behavior.
#
#         """
#         helper_functions.find_and_click_add_button(self.admin_browser, base_block)
#         block_model = parent_model_blocks[base_block]
#         child_blocks = block_model.child_blocks
#         for child_block in child_blocks:
#             self.model_router(child_blocks, child_block, -1)
#         helper_functions.find_and_click_toggle_button(self.admin_browser, depth)


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
#         admin_browser.visit(os.environ["LIVE_SERVER_URL"]+'/{}/pages/{}/'.format(ADMIN_SLUG, homepage.pk))
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
