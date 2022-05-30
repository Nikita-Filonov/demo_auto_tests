import uuid

import allure
import pytest
from alms_integration import create_objective

from base.api.base import BaseAPI
from base.api.users.objectives.objectives import get_objectives, update_objective, \
    get_objectives_query, get_objective, get_objective_objective_accesses, get_objective_objective_records, \
    get_objective_resource_link
from models.users.objective import Objectives
from models.users.role import Roles
from parameters.api.users.objectives import objective_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.objectives
@allure.epic('Core LMS')
@allure.feature('Objectives')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestObjectivesApi(BaseAPI):
    objective = Objectives.manager

    @allure.id("465")
    @allure.title('Get objectives (API)')
    def test_get_objectives(self):
        response = get_objectives()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.objective.to_array_schema)

    @allure.id("466")
    @pytest.mark.parametrize('query', to_sort_query(objective.to_json, exclude=objective.related_fields()))
    @allure.title('Query objectives (API)')
    def test_query_objectives(self, query):
        response = get_objectives_query(query)
        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("472")
    @allure.title('Get objective (API)')
    def test_get_objective(self, objective_function):
        response = get_objective(objective_function['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_json(json_response, objective_function)
        self.validate_json(json_response, self.objective.to_schema)

    @allure.id("471")
    @allure.title('Create objective (API)')
    def test_create_objective(self):
        objective_payload = self.objective.to_json

        response = create_objective(objective_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], objective_payload['id'], Objectives.objective_id.json)
        self.assert_attr(json_response['name'], objective_payload['name'], Objectives.name.json)
        self.assert_attr(json_response['code'], objective_payload['code'], Objectives.code.json)
        self.assert_attr(json_response['activity']['id'], objective_payload['activityId'], Objectives.activity_id.json)
        self.validate_json(json_response, self.objective.to_schema)

    @allure.id("473")
    @allure.title('Update objective (API)')
    def test_update_objective(self, objective_function):
        objective_payload = self.objective.to_json

        response = update_objective(objective_function['id'], objective_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], objective_function['id'], Objectives.objective_id.json)
        self.assert_attr(json_response['name'], objective_payload['name'], Objectives.name.json)
        self.assert_attr(json_response['code'], objective_payload['code'], Objectives.code.json)
        self.validate_json(json_response, self.objective.to_schema)

    @allure.id("470")
    @pytest.mark.parametrize('role_name', Roles.ROLES)
    @allure.title('Get objective resource link (API)')
    def test_get_objective_resource_link(self, objective_function, role_name):
        response = get_objective_resource_link(objective_function['id'], role_name)

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_truth(response.json()['token'], 'Resource link token')

    @allure.id("474")
    @allure.title('Get objective resource link negative (API)')
    @pytest.mark.parametrize('role', Roles.ROLES)
    def test_get_objective_resource_link_negative(self, role):
        objective_id = uuid.uuid4()
        response = get_objective_resource_link(objective_id, role)

        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("468")
    @allure.title('Get objective records (API)')
    def test_get_objective_records(self, objective_function):
        response = get_objective_objective_records(objective_function['id'])
        self.assert_response_status(response.status_code, self.http.OK)

    @allure.id("469")
    @allure.title('Get objective accesses (API)')
    def test_get_objective_accesses(self, objective_function):
        response = get_objective_objective_accesses(objective_function['id'])
        self.assert_response_status(response.status_code, self.http.OK)

    @allure.id("904")
    @allure.title('Check authorization for objectives endpoints (API)')
    @pytest.mark.parametrize('endpoint', objective_methods, ids=to_method_param)
    def test_check_authorization_for_user_roles_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
