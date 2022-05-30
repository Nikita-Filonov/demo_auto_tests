import uuid

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.roles.roles import get_roles, get_role, update_role, get_roles_query, get_role_permission, \
    get_role_permissions, create_role
from models.users.role import Roles, RolePermissions, SupportedRoles
from parameters.api.users.roles import roles_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param
from utils.utils import random_string, find


@pytest.mark.api
@pytest.mark.roles
@allure.epic('Core LMS')
@allure.feature('Roles')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestRolesApi(BaseAPI):
    role = Roles.manager
    role_permissions = RolePermissions.manager

    @allure.id("449")
    @allure.title('Get roles (API)')
    def test_get_roles(self):
        response = get_roles()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.role.to_array_schema)

    @allure.id("448")
    @allure.title('Query roles (API)')
    @pytest.mark.parametrize('query', to_sort_query(role.to_json, exclude=role.related_fields()))
    def test_query_roles(self, query):
        response = get_roles_query(query)

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("454")
    @allure.title('Get role (API)')
    def test_get_role(self, role):
        response = get_role(role['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], role['id'], Roles.role_id.json)
        self.assert_attr(json_response['name'], role['name'], Roles.name.json)
        self.validate_json(json_response, self.role.to_schema)

    @allure.id("453")
    @allure.title('Get role negative (API)')
    def test_get_role_negative(self):
        response = get_role(uuid.uuid4())
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("452")
    @allure.title('Get role permissions (API)')
    def test_get_role_permissions(self, role):
        response = get_role_permissions(role['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.role_permissions.to_array_schema)

    @allure.id("450")
    @allure.title('Get role permissions negative (API)')
    def test_get_role_permissions_negative(self):
        response = get_role_permissions(random_string())
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("446")
    @allure.title('Get role permission (API)')
    @pytest.mark.parametrize('role', SupportedRoles.to_list([SupportedRoles.OBSERVER]))
    def test_get_role_permission(self, role):
        role_id = find(lambda r: r['name'] == role, get_roles().json())['id']

        permissions_response = get_role_permissions(role_id)
        permissions_response_json = permissions_response.json()

        permission_response = get_role_permission(role_id, permissions_response_json[0]['id'])
        permission_response_json = permission_response.json()

        self.assert_response_status(permission_response.status_code, self.http.OK)
        self.assert_response_status(permissions_response.status_code, self.http.OK)
        self.assert_json(permission_response_json, permissions_response_json[0])
        self.validate_json(permission_response_json, self.role_permissions.to_schema)

    @allure.id("451")
    @allure.title('Get role permission negative (API)')
    def test_get_role_permission_negative(self):
        response = get_role_permission(random_string(), random_string())
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("756")
    @allure.title('Create role (API)')
    def test_create_role(self):
        payload = self.role.to_json

        response = create_role(payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], payload['id'], Roles.role_id.json)
        self.assert_attr(json_response['name'], payload['name'], Roles.name.json)
        self.assert_attr(json_response['tenant']['id'], payload['tenantId'], Roles.tenant_id.json)
        self.validate_json(json_response, self.role.to_schema)

    @allure.id("755")
    @allure.title('Update role (API)')
    def test_update_role(self, role):
        payload = self.role.to_json

        response = update_role(role['id'], payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], role['id'], Roles.role_id.json)
        self.assert_attr(json_response['name'], payload['name'], Roles.name.json)
        self.validate_json(json_response, self.role.to_schema)

    @allure.id("4512")
    @allure.title('Update role negative (API)')
    def test_update_role_negative(self, role):
        payload = self.role.to_negative_json()

        response = update_role(role['id'], payload)
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("913")
    @allure.title('Check authorization for roles endpoints (API)')
    @pytest.mark.parametrize('endpoint', roles_methods, ids=to_method_param)
    def test_check_authorization_for_roles_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
