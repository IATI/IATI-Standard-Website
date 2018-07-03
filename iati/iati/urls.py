"""Django URL settings. Defines the routing of user requests."""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns  # For internationalization
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from iati.activate_languages import i18n_patterns  # For internationalization

from home.views import reference_redirect


ADMIN_SLUG = "cms"


urlpatterns = [  # pylint: disable=invalid-name
    url(r'^django-{}/'.format(ADMIN_SLUG), admin.site.urls),
    url(r'^{}/'.format(ADMIN_SLUG), include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
]

urlpatterns += [
    url(r'^(101|102|103|104|105|201|202|203)/', reference_redirect)
]

urlpatterns += i18n_patterns(
    # These URLs will have /<language_code>/ appended to the beginning
    url(r'^search/$', search_views.search, name='search'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
)


if settings.DEBUG:
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
