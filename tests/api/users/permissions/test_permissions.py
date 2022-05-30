import uuid

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.permissions.permissions import get_permissions, update_permission, get_permission, \
    get_permissions_query, create_permission
from models.users.permission import Permissions
from parameters.api.users.permissions import permissions_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.permissions
@allure.epic('Core LMS')
@allure.feature('Permissions')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestPermissionsApi(BaseAPI):
    permission = Permissions.manager

    @allure.id("456")
    @allure.title('Get permissions (API)')
    def test_get_permissions(self):
        response = get_permissions()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.permission.to_array_schema)

    @allure.id("463")
    @allure.title('Create permission (API)')
    def test_create_permission(self):
        permission_payload = self.permission.to_json

        response = create_permission(permission_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['name'], permission_payload['name'], Permissions.name.json)
        self.assert_attr(json_response['scope'], permission_payload['scope'], Permissions.scope.json)
        self.assert_attr(json_response['scopeType'], permission_payload['scopeType'], Permissions.scope_type.json)
        self.assert_attr(json_response['tenant']['id'], permission_payload['tenantId'], Permissions.tenant_id.json)
        self.validate_json(json_response, self.permission.to_schema)

    @allure.id("460")
    @allure.title('Update permission (API)')
    def test_update_permission(self, permission):
        permission_payload = self.permission.to_json

        response = update_permission(permission['id'], permission_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], permission['id'], Permissions.permission_id.json)
        self.assert_attr(json_response['name'], permission_payload['name'], Permissions.name.json)
        self.assert_attr(json_response['scope'], permission_payload['scope'], Permissions.scope.json)
        self.assert_attr(json_response['scopeType'], permission_payload['scopeType'], Permissions.scope_type.json)
        self.assert_attr(json_response['tenant']['id'], permission_payload['tenantId'], Permissions.tenant_id.json)
        self.validate_json(json_response, self.permission.to_schema)

    @allure.id("455")
    @pytest.mark.parametrize('query', to_sort_query(permission.to_json, exclude=permission.related_fields()))
    @allure.title('Query permissions (API)')
    def test_query_permissions(self, query):
        response = get_permissions_query(query)

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("462")
    @allure.title('Get permission (API)')
    def test_get_permission(self, permission):
        response = get_permission(permission['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_json(json_response, permission)
        self.validate_json(json_response, self.permission.to_schema)

    @allure.id("457")
    @allure.title('Get permission negative (API)')
    def test_get_permission_negative(self):
        response = get_permission(uuid.uuid4())
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("909")
    @allure.title('Check authorization for permissions endpoints (API)')
    @pytest.mark.parametrize('endpoint', permissions_methods, ids=to_method_param)
    def test_check_authorization_for_permissions_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
