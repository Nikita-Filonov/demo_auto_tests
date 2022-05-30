import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.tenants.tenants import create_tenant, get_tenant, get_tenants, update_tenant, get_tenants_query
from models.users.tenant import Tenants
from parameters.api.users.tenants import tenant_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.tenants
@allure.epic('Core LMS')
@allure.feature('Tenants')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestTenantsApi(BaseAPI):
    tenant = Tenants.manager

    @allure.id("4158")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1265', name="Tenants. Admin can't create tenant.")
    @allure.title('Create tenant (API)')
    def test_create_tenant(self):
        payload = self.tenant.to_json
        response = create_tenant(payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], payload['id'], Tenants.tenant_id.json)
        self.assert_attr(json_response['name'], payload['name'], Tenants.name.json)
        self.validate_json(json_response, self.tenant.to_schema)

    @allure.id("4187")
    @pytest.mark.skip(reason='New created user can not setup a password')
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-982',
        name='New created user can not setup a password'
    )
    @allure.title('Create tenant and check Roles/Permissions (API)')
    def test_create_tenant_and_check_roles_permissions(self, tenant_function):
        pass

    @allure.id("4157")
    @allure.title('Get tenants (API)')
    def test_get_tenants(self):
        response = get_tenants()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.tenant.to_array_schema)

    @allure.id("4160")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1265', name="Tenants. Admin can't create tenant.")
    @allure.title('Update tenant (API)')
    def test_update_tenant(self, tenant_function):
        payload = self.tenant.to_json
        response = update_tenant(tenant_function['id'], payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], tenant_function['id'], Tenants.tenant_id.json)
        self.assert_attr(json_response['name'], payload['name'], Tenants.name.json)
        self.validate_json(json_response, self.tenant.to_schema)

    @allure.id("4159")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1265', name="Tenants. Admin can't create tenant.")
    @allure.title('Get tenant (API)')
    def test_get_tenant(self, tenant_function):
        response = get_tenant(tenant_function['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_json(json_response, tenant_function)
        self.validate_json(json_response, self.tenant.to_schema)

    @allure.id("4156")
    @allure.title('Query tenants (API)')
    @pytest.mark.parametrize('query', to_sort_query(tenant.to_json, exclude=tenant.related_fields()))
    def test_query_tenants(self, query):
        response = get_tenants_query(query)

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("4155")
    @allure.title('Check authorization for tenants endpoints (API)')
    @pytest.mark.parametrize('endpoint', tenant_methods, ids=to_method_param)
    def test_check_authorization_for_tenants_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
