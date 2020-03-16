"""A module of unit tests for guidance and support."""
import pytest
from django.http import HttpRequest
from django import forms

from .zendeskhelper import generate_ticket

LEGITIMATE_USER = {}
LEGITIMATE_USER['request'] = HttpRequest()
LEGITIMATE_USER['request'].path = "/en/a-test-path"
LEGITIMATE_USER['form'] = forms.Form()
LEGITIMATE_USER['form'].cleaned_data = {
    'phone': '',
    'email': 'test@user.com',
    'textarea': 'A very serious matter.',
    'name': 'A legitimate user'
}
LEGITIMATE_USER.expected_output = {
    'request': {
        'requester': {
            'name': 'A legitimate user',
            'email': 'test@user.com'
        },
        'comment': {
            'body': 'A request was sent from /en/a-test-path.\nA very serious matter.'
        },
        'subject': 'Automated request from A legitimate user'
    }
}


@pytest.mark.parametrize("user", [LEGITIMATE_USER])
def test_generate_ticket(user):
    """Test a ticket from a valid user and a spam bot."""
    ticket = generate_ticket(user['request'], user['form'])
    assert ticket == user.expected_output
