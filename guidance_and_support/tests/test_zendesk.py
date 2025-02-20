"""A module of unit tests for guidance and support."""
import copy
import pytest
from django.http import HttpRequest
from django import forms

from guidance_and_support.zendeskhelper import generate_ticket

LEGITIMATE_USER = {}
LEGITIMATE_USER['request'] = HttpRequest()
LEGITIMATE_USER['request'].META['SERVER_NAME'] = "iatistandard.org"
LEGITIMATE_USER['request'].META['SERVER_PORT'] = 80
LEGITIMATE_USER['request'].path = "/en/guidance/get-support/"
LEGITIMATE_USER['form'] = forms.Form()
LEGITIMATE_USER['form'].cleaned_data = {
    'phone': '',
    'referrer': '/en/a-test-path',
    'email': 'test@user.com',
    'query': 'A very serious matter.',
    'name': 'A legitimate user'
}
LEGITIMATE_USER['score'] = 1.0
LEGITIMATE_USER['expected_output'] = {
    'request': {
        'requester': {
            'name': 'A legitimate user',
            'email': 'test@user.com'
        },
        'comment': {
            'body': (
                'A request was sent from /en/guidance/get-support/. The sender was previously on /en/a-test-path.'
                '\nA very serious matter.'
            )
        },
        'subject': 'Automated request from A legitimate user'
    }
}
SPAM_BOT = {}
SPAM_BOT['request'] = HttpRequest()
SPAM_BOT['request'].META['SERVER_NAME'] = "iatistandard.org"
SPAM_BOT['request'].META['SERVER_PORT'] = 80
SPAM_BOT['request'].path = "/en/a-test-path"
SPAM_BOT['form'] = forms.Form()
SPAM_BOT['form'].cleaned_data = {
    'phone': '',
    'referrer': '/en/a-test-path',
    'email': 'test@user.com',
    'query': 'A very unserious matter.',
    'name': 'A not legitimate user'
}
SPAM_BOT['score'] = 0.0
SPAM_BOT['expected_output'] = False


@pytest.mark.django_db
@pytest.mark.parametrize("user", [LEGITIMATE_USER, SPAM_BOT])
def test_generate_ticket(user):
    """Test a ticket from a valid user and a spam bot."""
    ticket = generate_ticket(user['request'], user['form'], score=user['score'])
    assert ticket == user['expected_output']


@pytest.mark.django_db
def test_generate_ticket_with_referer_path_false():
    """
    Test a ticket request sent from get-support page without referer page.
    """
    user = copy.deepcopy(LEGITIMATE_USER)
    user['form'].cleaned_data['referrer'] = ''
    user['expected_output']['request']['comment']['body'] = (
        'A request was sent from /en/guidance/get-support/.\nA very serious matter.'
    )
    ticket = generate_ticket(
        user['request'],
        user['form'],
        score=user['score']
    )
    assert ticket == user['expected_output']
