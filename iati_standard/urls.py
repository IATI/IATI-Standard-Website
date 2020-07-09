"""Module for bespoke admin area URLs needed to trigger update."""
from django.conf.urls import url
from iati_standard.views import utils

app_name = 'iati_standard'
urlpatterns = [
    url(r'^update-profile-data/$', utils.on_update_request, name='on_update_request'),
    url(r'^get-update-progress/$', utils.get_update_progress, name='get_update_progress'),
]
