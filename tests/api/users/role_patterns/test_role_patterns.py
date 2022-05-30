import uuid

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.role_patterns.role_patterns import get_role_patterns, create_role_pattern, get_role_pattern, \
    update_role_pattern, delete_role_pattern, get_role_patterns_query
from models.users.role_pattern import RolePatterns
from parameters.api.users.role_pattern import role_pattern_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.role_patterns
@allure.epic('Core LMS')
@allure.feature('Role patterns')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestRolePatternsApi(BaseAPI):
    role_pattern = RolePatterns.manager

    @allure.id("496")
    @allure.title('Get role patterns (API)')
    def test_get_role_patterns(self):
        response = get_role_patterns()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.role_pattern.to_array_schema)

    @allure.id("496")
    @pytest.mark.parametrize('query', to_sort_query(role_pattern.to_json, exclude=role_pattern.related_fields()))
    @allure.title('Get role patterns query (API)')
    def test_get_role_patterns_query(self, query):
        response = get_role_patterns_query(query)

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("501")
    @allure.title('Get role pattern (API)')
    def test_get_role_pattern(self, role_pattern):
        response = get_role_pattern(role_pattern['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], role_pattern['id'], RolePatterns.name.json)
        self.assert_attr(json_response['name'], role_pattern['name'], RolePatterns.name.json)
        self.assert_attr(json_response['scopeType'], role_pattern['scopeType'], RolePatterns.scope_type.json)
        self.validate_json(json_response, self.role_pattern.to_schema)

    @allure.id("506")
    @allure.title('Get role pattern negative (API)')
    def test_get_role_pattern_negative(self):
        response = get_role_pattern(uuid.uuid4())
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("498")
    @allure.title('Create role pattern (API)')
    def test_create_role_pattern(self):
        role_pattern_payload = self.role_pattern.to_json

        response = create_role_pattern(role_pattern_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], role_pattern_payload['id'], RolePatterns.role_pattern_id.json)
        self.assert_attr(json_response['name'], role_pattern_payload['name'], RolePatterns.name.json)
        self.assert_attr(json_response['scopeType'], role_pattern_payload['scopeType'], RolePatterns.scope_type.json)
        self.validate_json(json_response, self.role_pattern.to_schema)

    @allure.id("500")
    @allure.title('Delete role pattern (API)')
    def test_delete_role_pattern(self, role_pattern):
        delete_role_pattern(role_pattern['id'])
        response = get_role_pattern(role_pattern['id'])

        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("505")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-632',
        name='Unable to update scopeType on "RolePatterns" model'
    )
    @allure.title('Update role pattern (API)')
    def test_update_role_pattern(self, role_pattern):
        payload = self.role_pattern.to_json

        response = update_role_pattern(role_pattern['id'], payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], role_pattern['id'], RolePatterns.role_pattern_id.json)
        self.assert_attr(json_response['name'], payload['name'], RolePatterns.name.json)
        self.assert_attr(json_response['scopeType'], role_pattern['scopeType'], RolePatterns.scope_type.json)
        self.validate_json(json_response, self.role_pattern.to_schema)

    @allure.id("4506")
    @pytest.mark.xfail(reason='Validations errors')
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1220', name='Validations errors')
    @allure.title('Update role pattern negative (API)')
    def test_update_role_pattern_negative(self, role_pattern):
        payload = self.role_pattern.to_negative_json()

        response = update_role_pattern(role_pattern['id'], payload)
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("911")
    @allure.title('Check authorization for role patterns endpoints (API)')
    @pytest.mark.parametrize('endpoint', role_pattern_methods, ids=to_method_param)
    def test_check_authorization_for_role_patterns_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
