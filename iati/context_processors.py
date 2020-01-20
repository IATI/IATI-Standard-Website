from tools.models import ToolsListingPage


def has_new_tools_page():
    """Return the first new tools page if it exists."""
    return ToolsListingPage.objects.live().first()


def globals(request):
    """Return a global context dictionary for use by templates."""
    return {
        'global': {
            'has_new_tools_page': has_new_tools_page(),
        },
    }
