"""View defintions for the search app."""

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from wagtail.core.models import Page
from wagtail.search.models import Query


def search(request):
    """Process a user input for a search query and return a page containing results."""
    per_page = 10
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, per_page)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
        'paginator': paginator,
    })
