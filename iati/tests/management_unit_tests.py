"""A module of unit tests for management commands."""
import json
import pytest
import responses
from django.core.management.base import CommandError
from home.management.commands.updatestatistics import ACTIVITY_URL, ORGANISATION_URL, get_total_num_activities, get_total_num_publishers
from base_functional_tests import TEST_DATA_DIR
from home.models import AbstractBasePage
from django.utils.text import slugify


@responses.activate
def test_update_statistics():
    """A quick test with a static export of registry data for valid sums."""
    with open(TEST_DATA_DIR + "activities.json") as json_file:
        responses.add(responses.GET, ACTIVITY_URL,
                      json=json.load(json_file), status=200)

    with open(TEST_DATA_DIR + "organisations.json") as json_file:
        responses.add(responses.GET, ORGANISATION_URL,
                      json=json.load(json_file), status=200)

    assert get_total_num_activities() == 18031
    assert get_total_num_publishers() == 5


@responses.activate
def test_update_statistics_error():
    """A test with error codes to see if command fails gracefully."""
    responses.add(responses.GET, ACTIVITY_URL, status=500, json={'error': 500})
    with pytest.raises(CommandError):
        get_total_num_activities()

    responses.add(responses.GET, ORGANISATION_URL, status=500, json={'error': 500})
    with pytest.raises(CommandError):
        get_total_num_publishers()


@pytest.mark.django_db
def test_clean_dashes():
    """Test to clean trailing and leading dashes from slugs."""
    page = AbstractBasePage(slug_en="--dashes-")
    page.clean()
    assert page.slug_en == "dashes"


@pytest.mark.django_db
def test_clean_whitespaces():
    """Test to clean trailing and leading dashes and whitespaces from slugs when titles have whitespace."""
    page = AbstractBasePage(title=" whitespaces ")
    page.slug_en = slugify(page.title, allow_unicode=True)
    page.clean()
    assert page.slug_en == "whitespaces"
