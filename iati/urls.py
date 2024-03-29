"""Django URL settings. Defines the routing of user requests."""

from django.conf import settings
from django.conf.urls import include
from django.urls import path, re_path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images.views.serve import serve

from .activate_languages import i18n_patterns  # For internationalization

urlpatterns = list()

if settings.DEBUG:
    # Debug toolbar
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [  # pylint: disable=invalid-name
    re_path(r'^django-{}/'.format(settings.ADMIN_SLUG), admin.site.urls),
    re_path(r'^{}/'.format(settings.ADMIN_SLUG), include(wagtailadmin_urls)),
    re_path(r'^{}/'.format(settings.DOCUMENTS_SLUG), include(wagtaildocs_urls)),
]

urlpatterns += i18n_patterns(
    # Wagtail sitemap
    re_path(r'^sitemap\.xml$', sitemap),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    re_path(r'', include(wagtail_urls)),
    re_path(r'^([^/]*)/(\d*)/([^/]*)/[^/]*$', serve, name='wagtailimages_serve'),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
)
