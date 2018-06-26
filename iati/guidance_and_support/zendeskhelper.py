def generate_ticket(request):
    """Generate a JSON formatted support ticket for Zendesk given a request object"""
    path = request.path
    captcha = request.POST['phone'] == ""
    email = request.POST['email']
    query = request.POST['textarea']
    name = request.POST.get('name', 'Anonymous requester')
    if captcha and email and query:
        request_obj = {
            "request": {
                "requester": {"name": name, "email": email},
                "subject": "Automated request from {}".format(name),
                "comment": {"body": "A request was sent from {}.\n{}".format(path, query)}
            }
        }
        return request_obj
    return False
