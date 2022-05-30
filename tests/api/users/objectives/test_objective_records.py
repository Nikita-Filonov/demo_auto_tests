import uuid

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.objectives.objective_records import get_objective_records_query, get_objective_records, \
    get_objective_record
from models.users.objective_records import ObjectiveRecords
from parameters.api.users.objective_records import objective_record_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.objective_records
@allure.epic('Core LMS')
@allure.feature('Objectives records')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestObjectivesRecordsApi(BaseAPI):
    objective_record = ObjectiveRecords.manager

    @allure.id("483")
    @allure.title('Get objective records (API)')
    def test_get_objective_records(self):
        response = get_objective_records()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.objective_record.to_array_schema)

    @allure.id("481")
    @allure.title('Query objective records (API)')
    @pytest.mark.parametrize('query', to_sort_query(objective_record.to_json,
                                                    exclude=objective_record.related_fields()))
    def test_get_objective_records_query(self, query):
        response = get_objective_records_query(query)
        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("480")
    @allure.title('Get objective records negative (API)')
    def test_get_objective_records_negative(self):
        response = get_objective_record(uuid.uuid4())
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("919")
    @allure.title('Check authorization for objective records endpoints (API)')
    @pytest.mark.parametrize('endpoint', objective_record_methods, ids=to_method_param)
    def test_check_authorization_for_objective_records_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
