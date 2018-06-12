"""A module of unit tests for management commands."""
import responses
import pytest
import json
from home.management.commands.updatestatistics import ACTIVITY_URL, ORGANISATION_URL, get_total_num_activities, get_total_num_publishers
from base_functional_tests import TEST_DATA_DIR


@pytest.mark.django_db
@responses.activate
def test_update_statistics():
    with open(TEST_DATA_DIR + "activities.json") as json_file:
        responses.add(responses.GET, ACTIVITY_URL,
                      json=json.load(json_file), status=200)

    with open(TEST_DATA_DIR + "organisations.json") as json_file:
        responses.add(responses.GET, ORGANISATION_URL,
                      json=json.load(json_file), status=200)

    assert get_total_num_activities() == 1074796
    assert get_total_num_publishers() == 769
