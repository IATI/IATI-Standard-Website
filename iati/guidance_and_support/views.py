from django.shortcuts import render


def guidance_and_support(request):
    return render(request, "guidance_and_support/guidance_and_support.html", {})
