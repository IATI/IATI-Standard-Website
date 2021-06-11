"""Module for bespoke admin area URLs needed to trigger update."""
from django.urls import re_path
from iati_standard.views import utils

app_name = 'iati_standard'
urlpatterns = [
    re_path(r'^update-profile-data/$', utils.on_update_request, name='on_update_request'),
    re_path(r'^get-update-progress/$', utils.get_update_progress, name='get_update_progress'),
]
