"""A module of functional tests for base site functionality."""
import os
import pytest
from conftest import LOCALHOST
from django.core.management import call_command
from django.apps import apps
from django.utils.text import slugify
from home.models import AbstractContentPage, IATIStreamBlock, HomePage
from wagtail.core.blocks import CharBlock
from about_functional_tests import publish_page, view_live_page
import string
import random
import pdb


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

    def collect_base_pages(self, base_page_class):
        """Given an app name, return models belonging to that app that inherit from AbstractContentPage"""
        models = []
        for model in apps.get_models():
            if issubclass(model, base_page_class):
                models.append(model)
        return models

    def test_content_pages(self, admin_browser):
        """
        Test templates for every content page.
        Fill in random content for every text field and test to see if it exists on the template.

        Todo:
            - Test non-text content
        """
        homepage = HomePage.objects.first()
        content_models = self.collect_base_pages(AbstractContentPage)
        for content_model in content_models:
            random_content = {}
            admin_browser.visit(os.environ["LIVE_SERVER_URL"]+'/admin/pages/3/')
            admin_browser.click_link_by_text('Add child page')
            verbose_page_name = content_model.get_verbose_name()
            if content_model.can_create_at(homepage):
                admin_browser.click_link_by_text(verbose_page_name)
                admin_browser.find_by_text('English').click()
                admin_browser.fill('title_en', verbose_page_name)
                for base_block in IATIStreamBlock.base_blocks:
                    block_model = IATIStreamBlock.base_blocks[base_block]
                    if isinstance(block_model, CharBlock):
                        add_button_class = ".action-add-block-{}".format(base_block)
                        add_button = admin_browser.find_by_css(add_button_class)[0]
                        scroll_and_click(admin_browser, add_button)
                        toggle_button = admin_browser.find_by_css(".toggle")[0]
                        scroll_and_click(admin_browser, toggle_button)
                        text_field = admin_browser.find_by_css(".fieldname-{} input".format(base_block))[0]
                        text_field_name = text_field.__dict__['_element'].get_attribute('name')
                        rs = random_string()
                        random_content[base_block] = rs
                        admin_browser.fill(text_field_name, rs)
                admin_browser.find_by_text('Promote').click()
                admin_browser.fill('slug_en', slugify(verbose_page_name))
                publish_page(admin_browser)
                view_live_page(admin_browser, verbose_page_name)
                for rc_key in random_content:
                    assert admin_browser.is_text_present(random_content[rc_key])
