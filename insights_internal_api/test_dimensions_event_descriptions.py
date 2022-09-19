import json
import logging
import os
import sys
import time
import unittest

import requests

# fetch config
insights_internal_api = os.getenv('INSIGHTS_INTERNAL_API')
int_insights_org_id = os.getenv('INT_INSIGHTS_ORG_ID')


class TestDimensionEndpoints():

    def test_get_event_descriptions_valid(self):
        """
        """
        # set up
        org_id = int_insights_org_id

        # call
        res = requests.get(f"{insights_internal_api}/api/dimensions/event-descriptions/{org_id}")
        assert res.status_code == 200
        res_json = res.json()
        res_first_entry = res_json[0]
        res_columns = list(res_first_entry)

        # validate
        assert sorted(res_columns) == ['EventName', 'EventTypeId', 'GroupId', 'MetricType', 'UnitType']

    def test_get_event_descriptions_invalid_org(self):
        """
        """
        # set up
        org_id = "123abc"

        # call
        res = requests.get(f"{insights_internal_api}/api/dimensions/event-descriptions/{org_id}")
        assert res.status_code == 400
        res_json = res.json()

        # validate
        assert res_json['title'] == 'One or more validation errors occurred.'
        assert res_json['errors'] == {'groupId': ["The value '123abc' is not valid."]}
