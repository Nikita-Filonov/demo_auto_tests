import uuid

import allure
import pytest
from alms_integration import create_objective_access

from base.api.base import BaseAPI
from base.api.users.objectives.objective_accesses import get_objective_accesses, delete_objective_access, \
    get_objective_access, get_objective_accesses_query
from models.users.objective_access import ObjectiveAccesses
from parameters.api.users.objective_accesses import objective_access_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.objective_accesses
@allure.epic('Core LMS')
@allure.feature('Objective accesses')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestObjectiveAccessesApi(BaseAPI):
    objective_access = ObjectiveAccesses.manager

    @allure.id("486")
    @allure.title('Get objective accesses (API)')
    def test_get_objective_accesses(self):
        response = get_objective_accesses()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.objective_access.to_array_schema)

    @allure.id("568")
    @allure.title('Create objective access (API)')
    def test_create_objective_access(self):
        objective_access_payload = self.objective_access.to_json

        response = create_objective_access(objective_access_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], objective_access_payload['id'],
                         ObjectiveAccesses.objective_access_id.json)
        self.assert_attr(json_response['objectiveId'], objective_access_payload['objectiveId'],
                         ObjectiveAccesses.objective_id.json)
        self.assert_attr(json_response['tenantId'], objective_access_payload['tenantId'],
                         ObjectiveAccesses.tenant_id.json)
        self.validate_json(json_response, self.objective_access.to_schema)

    @allure.id("4504")
    @allure.title('Create objective access negative (API)')
    def test_create_objective_access_negative(self):
        objective_access_payload = self.objective_access.to_negative_json()

        response = create_objective_access(objective_access_payload)
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("487")
    @allure.title('Delete objective access (API)')
    def test_delete_objective_access(self, objective_access):
        delete_objective_access(objective_access['id'])
        response = get_objective_access(objective_access['id'])

        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("488")
    @allure.title('Delete objective access negative (API)')
    def test_delete_objective_access_negative(self):
        objective_access_id = str(uuid.uuid4())
        response = delete_objective_access(objective_access_id)
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("486")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-241',
        name='Endpoint /objective-accesses/{id} returns 404'
    )
    @allure.title('Get objective access (API)')
    def test_get_objective_access(self, objective_access):
        response = get_objective_access(objective_access['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], objective_access['id'], ObjectiveAccesses.objective_access_id.json)
        self.assert_attr(json_response['objectiveId'], objective_access['objectiveId'],
                         ObjectiveAccesses.objective_id.json)
        self.assert_attr(json_response['tenantId'], objective_access['tenantId'],
                         ObjectiveAccesses.tenant_id.json)
        self.validate_json(json_response, self.objective_access.to_schema)

    @allure.id("1889")
    @pytest.mark.parametrize('query', to_sort_query(objective_access.to_json,
                                                    exclude=objective_access.related_fields()))
    @allure.title('Query objective accesses (API)')
    def test_query_objective_accesses(self, query):
        response = get_objective_accesses_query(query)
        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("921")
    @allure.title('Check authorization for objective accesses endpoints (API)')
    @pytest.mark.parametrize('endpoint', objective_access_methods, ids=to_method_param)
    def test_check_authorization_for_objective_accesses_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
