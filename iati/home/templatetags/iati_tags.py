from django import template
from events.models import EventIndexPage

register = template.Library()

@register.simple_tag(takes_context=True)
def events_index_page_url(context):
    events_index_page = EventIndexPage.objects.live().first()
    if events_index_page is not None:
        return events_index_page.get_url(context['request'])
    else:
        return ""