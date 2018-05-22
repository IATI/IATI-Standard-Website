"""A module of functional tests for base site functionality."""
import os
import pytest
from conftest import LOCALHOST
from django.core.management import call_command
from django.apps import apps
from django.utils.text import slugify
from django.conf import settings
from home.models import AbstractContentPage, IATIStreamBlock, HomePage
from wagtail.core.blocks import CharBlock, RichTextBlock, StreamBlock
from wagtail.documents.blocks import DocumentChooserBlock
from about_functional_tests import view_live_page
import string
import random
import pdb


def collect_base_pages(base_page_class):
    """Given an base page class, return models belonging to that app that inherit from AbstractContentPage"""
    models = list()
    for model in apps.get_models():
        if issubclass(model, base_page_class):
            models.append(model)
    return models


def random_string(size=10, chars=string.ascii_uppercase+string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def click_obscured(admin_browser, element):
    """A function that clicks elements even if they're slightly obscured"""
    admin_browser.driver.execute_script("arguments[0].click();", element.__dict__['_element'])


def scroll_to_element(admin_browser, element):
    """A function that scrolls to the location of an element"""
    rect = element.__dict__['_element'].rect
    mid_point_x = int(rect['x'] + (rect['width']/2))
    mid_point_y = int(rect['y'] + (rect['height']/2))
    admin_browser.driver.execute_script("window.scrollTo({}, {});".format(mid_point_x, mid_point_y))


def scroll_and_click(admin_browser, element):
    """A function that scrolls to, and clicks an element"""
    scroll_to_element(admin_browser, element)
    click_obscured(admin_browser, element)


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


@pytest.mark.django_db()
class TestContentEditor():
    """A container for testing models that incorporate the default content editor"""

    def find_and_click_add_button(self, admin_browser, base_block):
        add_button_class = ".action-add-block-{}".format(base_block)
        add_button = admin_browser.find_by_css(add_button_class)[0]
        scroll_and_click(admin_browser, add_button)

    def find_and_click_toggle_button(self, admin_browser, toggle_index):
        toggle_button = admin_browser.find_by_css(".toggle")[toggle_index]
        scroll_and_click(admin_browser, toggle_button)

    def fill_content_editor_block(self, admin_browser, base_block, text_field_class, content):
        full_text_field_class = ".fieldname-{}".format(base_block)+text_field_class
        text_field = admin_browser.find_by_css(full_text_field_class)[0]
        scroll_and_click(admin_browser, text_field)
        text_field.fill(content)

    @pytest.mark.parametrize('content_model', collect_base_pages(AbstractContentPage))
    def test_content_pages(self, admin_browser, content_model):
        """
        Test templates for every content page.
        Fill in random content for every text field and test to see if it exists on the template.

        Todo:
            - Test non-text content
        """
        homepage = HomePage.objects.first()
        random_content = dict()
        admin_browser.visit(os.environ["LIVE_SERVER_URL"]+'/admin/pages/{}/'.format(homepage.pk))
        admin_browser.click_link_by_text('Add child page')
        verbose_page_name = content_model.get_verbose_name()
        if content_model.can_create_at(homepage):
            admin_browser.click_link_by_text(verbose_page_name)
            admin_browser.find_by_text('English').click()
            admin_browser.fill('title_en', verbose_page_name)
            for base_block in IATIStreamBlock.base_blocks:
                block_model = IATIStreamBlock.base_blocks[base_block]
                if isinstance(block_model, CharBlock):
                    rs = random_string()
                    random_content[base_block] = rs
                    self.find_and_click_add_button(admin_browser, base_block)
                    self.find_and_click_toggle_button(admin_browser, 0)
                    self.fill_content_editor_block(admin_browser, base_block, " input", rs)
                if isinstance(block_model, RichTextBlock):
                    rs = random_string()
                    random_content[base_block] = rs
                    self.find_and_click_add_button(admin_browser, base_block)
                    self.find_and_click_toggle_button(admin_browser, 0)
                    self.fill_content_editor_block(admin_browser, base_block, " .public-DraftEditor-content", rs)
                if isinstance(block_model, StreamBlock):
                    self.find_and_click_add_button(admin_browser, base_block)
                    child_blocks = block_model.child_blocks
                    for child_block in child_blocks:
                        child_block_model = block_model.child_blocks[child_block]
                        if isinstance(child_block_model, CharBlock):
                            rs = random_string()
                            random_content[child_block] = rs
                            self.find_and_click_add_button(admin_browser, child_block)
                            self.find_and_click_toggle_button(admin_browser, 1)
                            self.fill_content_editor_block(admin_browser, child_block, " input", rs)
                        if isinstance(child_block_model, DocumentChooserBlock):
                            self.find_and_click_add_button(admin_browser, child_block)
                            choose_doc_button = admin_browser.find_by_text("Choose a document")[0]
                            scroll_and_click(admin_browser, choose_doc_button)
                            random_content[child_block] = "Annual report"
                            annual_report_link = admin_browser.find_by_text("Annual report")
                            if len(annual_report_link) > 0:
                                scroll_and_click(admin_browser, annual_report_link[0])
                            else:
                                upload_tab, upload_button = admin_browser.find_by_text('Upload')
                                scroll_and_click(admin_browser, upload_tab)
                                title_field = admin_browser.find_by_xpath("//input[@name='title']")[0]
                                scroll_and_click(admin_browser, title_field)
                                title_field.fill('Annual report')
                                admin_browser.attach_file('file', settings.BASE_DIR+"/tests/data/annual-report.pdf")
                                scroll_and_click(admin_browser, upload_button)
                    self.find_and_click_toggle_button(admin_browser, 0)

            promote_tab = admin_browser.find_by_text('Promote')[0]
            scroll_and_click(admin_browser, promote_tab)
            admin_browser.fill('slug_en', slugify(verbose_page_name))
            publish_arrow = admin_browser.find_by_xpath('//div[@class="dropdown-toggle icon icon-arrow-up"]')[0]
            scroll_and_click(admin_browser, publish_arrow)
            publish_button = admin_browser.find_by_text('Publish')[0]
            scroll_and_click(admin_browser, publish_button)
            page_link = admin_browser.find_by_text(verbose_page_name)[0]
            scroll_to_element(admin_browser, page_link)
            page_link.mouse_over()
            button_link = admin_browser.find_by_text('View live')
            href = button_link[0].__dict__['_element'].get_property('href')
            admin_browser.visit(href)
            for rc_key in random_content:
                assert admin_browser.is_text_present(random_content[rc_key])
