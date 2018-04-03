from django.shortcuts import render

from wagtail.core.models import Page

def about(request):
    return render(request, "about.html", {})
