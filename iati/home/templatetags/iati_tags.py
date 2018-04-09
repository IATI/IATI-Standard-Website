import os
from django import template
from events.models import EventIndexPage

register = template.Library()

@register.simple_tag(takes_context=True)
def events_index_page_url(context):
    """Returns the relative url for the events index page"""
    events_index_page = EventIndexPage.objects.live().first()
    if events_index_page is not None:
        return events_index_page.get_url(context['request'])
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
