"""A module to contain helper function to format data for ZenDesk."""


def generate_ticket(request):
    """Generate a JSON formatted support ticket for Zendesk given a request object.

    Phone field is hidden to users, and hopefully captures spam content.
    If the phone field is filled at all, treat the request as spam.

    Args:
        request (django.http.HttpRequest): A django request containing the user's POSTed content.

    """
    path = request.path
    is_honeypot_valid = request.POST['phone'] == ""  # Set to False if honeypot is entered
    email = request.POST['email']
    query = request.POST['textarea']
    name = request.POST.get('name', 'Anonymous requester')
    if is_honeypot_valid and email and query:
        request_obj = {
            "request": {
                "requester": {"name": name, "email": email},
                "subject": "Automated request from {}".format(name),
                "comment": {"body": "A request was sent from {}.\n{}".format(path, query)}
            }
        }
        return request_obj
    return False
