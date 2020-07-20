"""A module to contain helper function to format data for ZenDesk."""
from django.conf import settings
from home.models import SpamSettings


def generate_ticket(request, form, score=None, suspicious=False):
    """Generate a JSON formatted support ticket for Zendesk given a request object.

    Args:
        request (django.http.HttpRequest): A django request.
        form (django.forms.Form): A django form containing the user's content.
        score: captcha v3 score if any
        suspicious: boolean, whether the submission is suspicious

    """
    spam_settings = SpamSettings.for_request(request)
    if score <= spam_settings.spam_threshold:
        return False
    path = request.path
    email = form.cleaned_data.get('email')
    query = form.cleaned_data.get('query')
    name = form.cleaned_data.get('name', 'Anonymous requester')
    if email and query:
        request_obj = {
            "request": {
                "requester": {
                    "name": name,
                    "email": email
                },
                "subject": "Automated request from {}".format(name),
                "comment": {
                    "body": "A request was sent from {}.\n{}".format(path, query)
                }
            }
        }
        if suspicious:
            request_obj['request']['custom_fields'] = [
                {
                    "id": settings.ZENDESK_CAPTCHA_FIELD_ID,
                    "value": score
                },
                {
                    "id": settings.ZENDESK_SUSPICIOUS_FIELD_ID,
                    "value": "true"
                }
            ]

        return request_obj

    return False
