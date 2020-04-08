"""Module of context processors for the IATI Standard Website."""

import itertools
from django.conf import settings
from wagtail.core.models import Page
from navigation.models import (
    PrimaryMenu,
    UtilityMenu,
    UsefulLinks,
)
from search.models import SearchPage
from guidance_and_support.models import SupportPage


def get_current_page(request):
    """Try and get a page safely."""
    try:
        # this try is here to protect against 500 errors when there is a 404 error
        # taken from https://github.com/torchbox/wagtail/blob/master/wagtail/wagtailcore/views.py#L17
        path_components = [component for component in request.path.split('/') if component]
        current_page, args, kwargs = request.site.root_page.specific.route(request, path_components[1:])
        return current_page
    except Exception:
        return None


def captchakey(request):
    """Return the public captcha key."""
    return {'RECAPTCHA_KEY': settings.RECAPTCHA_PUBLIC_KEY}


def globals(request):
    """Return a global context dictionary for use by templates."""
    current_page = get_current_page(request)
    search_page = SearchPage.objects.all().live().first()
    support_page = SupportPage.objects.all().live().first()

    return {
        'global': {
            'primary_menu': construct_nav(PrimaryMenu.for_site(request.site).primary_menu_links.all(), current_page),
            'utility_menu': construct_nav(UtilityMenu.for_site(request.site).utility_menu_links.all(), current_page),
            'useful_links': UsefulLinks.for_site(request.site).useful_links.all(),
            'twitter_handle': settings.TWITTER_HANDLE,
            'search_page': search_page if search_page else current_page,
            'support_page': support_page if support_page else current_page,
        },
    }


def construct_nav(qs, current_page):
    """Construct a navigation menu."""
    nav = list(qs)
    for item in nav:
        item.active = False
        try:
            if Page.objects.filter(id=item.page.id).ancestor_of(current_page, inclusive=True).first():
                item.active = True
        except AttributeError:
            pass

    for a, b in itertools.combinations(nav, 2):
        if a.active and b.active:
            if a.page.depth > b.page.depth:
                b.active = False
            else:
                a.active = False

    return nav
