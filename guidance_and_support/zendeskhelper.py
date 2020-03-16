"""A module to contain helper function to format data for ZenDesk."""


def generate_ticket(request, form, score=None, suspicious=False):
    """Generate a JSON formatted support ticket for Zendesk given a request object.

    Args:
        request (django.http.HttpRequest): A django request.
        form (django.forms.Form): A django form containing the user's content.
        score: captcha v3 score if any
        suspicious: boolean, whether the submission is suspicious

    """
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
                    "id": 360005962277,
                    "value": score
                },
                {
                    "id": 360005946038,
                    "value": "true"
                }
            ]

        return request_obj

    return False
