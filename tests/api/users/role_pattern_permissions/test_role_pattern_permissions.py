import uuid

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.role_pattern_permissions.role_pattern_permissions import create_role_pattern_permission, \
    get_role_pattern_permission, delete_role_pattern_permission, get_role_pattern_permissions_query, \
    get_role_pattern_permissions
from models.users.role_pattern_permission import RolePatternPermissions
from parameters.api.users.role_pattern_permissions import role_pattern_permission_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param
from utils.utils import random_string


@pytest.mark.api
@pytest.mark.role_pattern_permissions
@allure.epic('Core LMS')
@allure.feature('Role pattern permissions')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestRolePatternPermissionsApi(BaseAPI):
    role_pattern_permission = RolePatternPermissions.manager

    @allure.id("513")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-990',
        name='Scope always null when creating role pattern permission'
    )
    @allure.title('Get role pattern permissions (API)')
    def test_get_role_pattern_permissions(self):
        response = get_role_pattern_permissions()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.role_pattern_permission.to_array_schema)

    @allure.id("514")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-990',
        name='Scope always null when creating role pattern permission'
    )
    @allure.title('Create role pattern permission (API)')
    def test_create_role_pattern_permission(self):
        payload = self.role_pattern_permission.to_dict()

        response = create_role_pattern_permission(payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], payload['id'], RolePatternPermissions.role_pattern_permission_id.json)
        self.assert_attr(json_response['name'], payload['name'], RolePatternPermissions.name.json)
        self.assert_attr(json_response['scope'], payload['scope'], RolePatternPermissions.scope.json)
        self.assert_attr(json_response['scopeType'], payload['scopeType'], RolePatternPermissions.scope_type.json)
        self.assert_attr(json_response['rolePattern']['id'], payload['rolePatternId'],
                         RolePatternPermissions.role_pattern_id.json)
        self.validate_json(json_response, self.role_pattern_permission.to_schema)

    @allure.id("509")
    @allure.title('Query role pattern permissions (API)')
    @pytest.mark.parametrize('query', to_sort_query(role_pattern_permission.to_json,
                                                    exclude=role_pattern_permission.related_fields()))
    def test_query_role_pattern_permissions(self, query):
        response = get_role_pattern_permissions_query(query)
        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("508")
    @allure.title('Delete role pattern permission (API)')
    def test_delete_role_pattern_permission(self, role_pattern_permission):
        delete_role_pattern_permission(role_pattern_permission['id'])
        response = get_role_pattern_permission(role_pattern_permission['id'])

        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("518")
    @allure.title('Delete role pattern permission negative (API)')
    def test_delete_role_pattern_permission_negative(self):
        response = delete_role_pattern_permission(random_string())
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("510")
    @allure.title('Get role pattern permission (API)')
    def test_get_role_pattern_permission(self, role_pattern_permission):
        response = get_role_pattern_permission(role_pattern_permission['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['name'], role_pattern_permission['name'],
                         RolePatternPermissions.name.json)
        self.assert_attr(json_response['scope'], role_pattern_permission['scope'],
                         RolePatternPermissions.name.json)
        self.assert_attr(json_response['scopeType'], role_pattern_permission['scopeType'],
                         RolePatternPermissions.scope_type.json)
        self.assert_attr(json_response['rolePattern']['id'], role_pattern_permission['rolePattern']['id'],
                         RolePatternPermissions.role_pattern_id.json)
        self.validate_json(json_response, self.role_pattern_permission.to_schema)

    @allure.id("516")
    @allure.title('Get role pattern permission negative (API)')
    def test_get_role_pattern_permission_negative(self):
        response = get_role_pattern_permission(uuid.uuid4())
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("906")
    @allure.title('Check authorization for role pattern permissions endpoints (API)')
    @pytest.mark.parametrize('endpoint', role_pattern_permission_methods, ids=to_method_param)
    def test_check_authorization_for_role_pattern_permissions_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
