from tools.models import ToolsListingPage


def has_new_tools_page():
    return ToolsListingPage.objects.live().first()


def globals(request):

    return {
        'global': {
            'has_new_tools_page': has_new_tools_page(),
        },
    }
