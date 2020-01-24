from tools.models import ToolsListingPage
from django.conf import settings


def has_new_tools_page():
    """Return the first new tools page if it exists."""
    return ToolsListingPage.objects.live().first()


def captchakey(request):
    """Return the public captcha key."""
    return {'RECAPTCHA_KEY': settings.RECAPTCHA_PUBLIC_KEY}


def globals(request):
    """Return a global context dictionary for use by templates."""
    return {
        'global': {
            'has_new_tools_page': has_new_tools_page(),
        },
    }
