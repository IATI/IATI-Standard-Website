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

register = template.Library()

@register.simple_tag(takes_context=True)
def default_page_url(context, default_page_name="home"):
    """Returns the relative url for a top-level default page"""
    if default_page_name == "about":
        default_page = AboutPage.objects.live().first()
    elif default_page_name == "contact":
        default_page = ContactPage.objects.live().first()
    elif default_page_name == "events":
        default_page = EventIndexPage.objects.live().first()
    elif default_page_name == "guidance_and_support":
        default_page = GuidanceAndSupportPage.objects.live().first()
    elif default_page_name == "news":
        default_page = NewsIndexPage.objects.live().first()
    else:
        default_page = HomePage.objects.live().first()
    if default_page is not None:
        return default_page.get_url(context['request'])
    return ""

def humansize(nbytes):
    """Short function to turn bytes into a human readable string. Could break if we start hosting exabyte files"""
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    formatted_xbytes = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (formatted_xbytes, suffixes[i])

@register.filter
def filesize(value):
    """Returns the filesize of the filename given in value"""
    return humansize(os.path.getsize(value))

@register.inclusion_tag("home/includes/translation_links.html",takes_context=True)
def translation_links(context, calling_page):
    """Takes the inclusion template 'translation_links.html' and returns a snippet of HTML with links to the requesting page in all offered languages"""
    language_results = []
    for language_code, language_name in settings.LANGUAGES:
        with use_language(language_code):
            language_url = pageurl(context,calling_page)
            language_results.append({"code": language_code, "name": language_name, "url": language_url})

    return {
        'languages': language_results,
    }
