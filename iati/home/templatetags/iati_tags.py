import os
from django import template
from home.models import HomePage
from about.models import AboutPage
from contact.models import ContactPage
from events.models import EventIndexPage
from guidance_and_support.models import GuidanceAndSupportPage
from news.models import NewsIndexPage

from django.conf import settings
from wagtail_modeltranslation.contextlib import use_language
from wagtail.core.templatetags.wagtailcore_tags import pageurl

import pdb

register = template.Library()

@register.simple_tag(takes_context=True)
def default_page_url(context, default_page_name="home"):
    """Returns the relative url for a top-level default page"""
    page_model_names = {
        'home': HomePage,
        'about': AboutPage,
        'contact': ContactPage,
        'events': EventIndexPage,
        'guidance_and_support': GuidanceAndSupportPage,
        'news': NewsIndexPage,
    }

    default_page = page_model_names[default_page_name].objects.live().first()

    if default_page is None:
        return ''
    return default_page.get_url(context['request'])

@register.inclusion_tag("home/includes/translation_links.html",takes_context=True)
def translation_links(context, calling_page):
    """Takes the inclusion template 'translation_links.html' and returns a snippet of HTML with links to the requesting page in all offered languages"""
    language_results = []
    for language_code, language_name in settings.LANGUAGES:
        with use_language(language_code):
            language_url = pageurl(context, calling_page)
            language_results.append({"code": language_code, "name": language_name, "url": language_url})

    return {
        'languages': language_results,
    }


def discover_tree_recursive(current_page, calling_page):
    parent_menu = []
    if current_page.depth > calling_page.depth:
        return parent_menu
    for child in current_page.get_children().specific().live():
        page_dict = {
            'page_title': child.heading if child.heading else child.page_title,
            'page_slug': child.slug,
            'page_depth': child.depth,
            'is_active': (current_page in calling_page.get_ancestors()) or (current_page == calling_page)
        }
        parent_menu.append(page_dict)
        if page_dict['is_active']:
            child_menu = discover_tree_recursive(child, calling_page)
        return parent_menu + child_menu


@register.inclusion_tag('home/includes/sidepanel.html')
def side_panel(calling_page):
    """Returns the side panel given the about hierarchy"""
    if calling_page.depth <= 3:  # If the page where this is called is already a main section of the site (e.g. About page)
        main_section = calling_page
    else:
        home_page = HomePage.objects.live().first()
        main_section = home_page.get_children().ancestor_of(calling_page).live().first().specific()

    menu_to_display = discover_tree_recursive(main_section, calling_page)
    pdb.set_trace()

    # [
    #     {
    #         'page_title': 'Why aid transparency matters',
    #         'page_slug': 'why_aid_matters',
    #         'page_depth': 4,
    #         'is_active': False
    #     },
    #     {
    #         'page_title': 'Governance',
    #         'page_slug': 'governance',
    #         'page_depth': 4,
    #         'is_active': True
    #     },
    #     {
    #         'page_title': 'IATI',
    #         'page_slug': 'governance-iati',
    #         'page_depth': 5,
    #         'is_active': True
    #     },
    #     {
    #         'page_title': 'UNDP',
    #         'page_slug': 'governance-undp',
    #         'page_depth': 5,
    #         'is_active': False
    #     },
    #     {
    #         'page_title': 'People',
    #         'page_slug': 'people',
    #         'page_depth': 4,
    #         'is_active': False
    #     },
    # ]

    return {"ancestors_children": main_section.menu_order.all, "calling_page": calling_page}
