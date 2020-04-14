"""Django URL settings. Defines the routing of user requests."""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images.views.serve import serve

from .activate_languages import i18n_patterns  # For internationalization


urlpatterns = [  # pylint: disable=invalid-name
    url(r'^django-{}/'.format(settings.ADMIN_SLUG), admin.site.urls),
    url(r'^{}/'.format(settings.ADMIN_SLUG), include(wagtailadmin_urls)),
    url(r'^{}/'.format(settings.DOCUMENTS_SLUG), include(wagtaildocs_urls)),
]


urlpatterns += i18n_patterns(
    # Wagtail sitemap
    url(r'^sitemap\.xml$', sitemap),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),
    url(r'^([^/]*)/(\d*)/([^/]*)/[^/]*$', serve, name='wagtailimages_serve'),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
)


if settings.DEBUG:
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
