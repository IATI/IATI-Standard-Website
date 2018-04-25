import os
from django import template
from wagtail.core.models import Page
from home.models import HomePage
from about.models import AboutPage
from contact.models import ContactPage
from events.models import EventIndexPage
from guidance_and_support.models import GuidanceAndSupportPage
from news.models import NewsIndexPage

from django.conf import settings
from wagtail_modeltranslation.contextlib import use_language
from wagtail.core.templatetags.wagtailcore_tags import pageurl

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


@register.filter
def subtract(value, arg):
    """In-template subtraction"""
    return value - arg


@register.inclusion_tag('home/includes/sidepanel.html')
def side_panel(calling_page):
    """Returns the side panel given the about hierarchy"""
    if calling_page.depth <= 3:
        highest_ancestor = calling_page
    else:
        home_page = HomePage.objects.live().first()
        highest_ancestor = home_page.get_children().ancestor_of(calling_page).live().first().specific()
    return {"ancestors_children": highest_ancestor.menu_order.all, "calling_page": calling_page}

@register.inclusion_tag("home/includes/translation_links.html", takes_context=True)
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
