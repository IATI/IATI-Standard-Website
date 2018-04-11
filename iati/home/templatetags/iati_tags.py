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

from django.utils import timezone
import pytz
from django.template.defaultfilters import date as _date

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
            language_url = pageurl(context, calling_page)
            language_results.append({"code": language_code, "name": language_name, "url": language_url})

    return {
        'languages': language_results,
    }

@register.filter
def haspassed(value):
    """Takes a date and tells you if it's in the past"""
    now = timezone.now()
    return value < now

@register.filter
def twopartdate(date_start, date_end):
    """Takes two datetimes and determines whether to display start and end times, or start and end dates.

    If an end date exists, we can compare the two dates.
    If the two dates are the same, localize the date for the first part and stringify the time range for the second.
    If the two dates are not the same, part 2 becomes the second date.

    If no end date exists, part 2 is just the start time.
    """
    part1 = _date(date_start, "DATE_FORMAT")
    enDash = u'\u2013'
    if date_end:
        if date_start.date() == date_end.date():
            part2 = "{0}{1}{2}".format(_date(date_start, "TIME_FORMAT"), enDash, _date(date_end, "TIME_FORMAT"))
            part2_is_time = True
        else:
            part2 = _date(date_end, "DATE_FORMAT")
            part2_is_time = False
    else:
        part2 = _date(date_start, "TIME_FORMAT")
        part2_is_time = True
    return {"part1":part1, "part2":part2, "part2_is_time":part2_is_time}
