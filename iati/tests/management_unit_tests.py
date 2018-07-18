"""A module of unit tests for management commands."""
import json
import pytest
import responses
from django.core.management.base import CommandError
from home.management.commands.updatestatistics import ACTIVITY_URL, ORGANISATION_URL, get_total_num_activities, get_total_num_publishers
from tests import helper_functions


@responses.activate
def test_update_statistics():
    """A quick test with a static export of registry data for valid sums."""
    with open(helper_functions.TEST_DATA_DIR + "activities.json") as json_file:
        responses.add(responses.GET, ACTIVITY_URL,
                      json=json.load(json_file), status=200)

    with open(helper_functions.TEST_DATA_DIR + "organisations.json") as json_file:
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
