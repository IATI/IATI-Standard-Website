"""A module to contain helper function to format data for ZenDesk."""
import urllib
import json

from django.conf import settings


def generate_ticket(request, form):
    """Generate a JSON formatted support ticket for Zendesk given a request object.

    Args:
        request (django.http.HttpRequest): A django request.
        form (django.forms.Form): A django form containing the user's content.

    """
    if form.cleaned_data.get('skip_captcha_check'):
        result = True
    else:
        return True
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())['success']
    if result:
        path = request.path
        # is_honeypot_valid = form.cleaned_data.get('phone') == ""  # Set to False if honeypot is entered
        email = form.cleaned_data.get('email')
        query = form.cleaned_data.get('query')
        name = form.cleaned_data.get('name', 'Anonymous requester')
        if email and query:
            request_obj = {
                "request": {
                    "requester": {"name": name, "email": email},
                    "subject": "Automated request from {}".format(name),
                    "comment": {"body": "A request was sent from {}.\n{}".format(path, query)}
                }
            }
            return request_obj
    return False
