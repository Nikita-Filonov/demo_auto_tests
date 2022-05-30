import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.tenant_settings.tenant_settings import get_tenant_settings, create_tenant_setting, \
    update_tenant_setting, delete_tenant_setting, get_tenant_setting, get_tenant_settings_query
from models.users.tenant_setting import TenantSettings
from parameters.api.users.tenant_settings import tenant_settings_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.tenant_settings
@allure.epic('Core LMS')
@allure.feature('Tenant settings')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestTenantSettingsApi(BaseAPI):
    tenant_setting = TenantSettings.manager

    @allure.id("4391")
    @allure.title('Get tenant settings (API)')
    def test_get_tenant_settings(self):
        response = get_tenant_settings()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.tenant_setting.to_array_schema)

    @allure.id("4394")
    @allure.title('Create tenant setting (API)')
    def test_create_tenant_setting(self):
        tenant_setting_payload = self.tenant_setting.to_json

        response = create_tenant_setting(tenant_setting_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_json(tenant_setting_payload, json_response)
        self.validate_json(json_response, self.tenant_setting.to_schema)

    @allure.id("4389")
    @pytest.mark.xfail(reason='Validations errors')
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1220', name='Validations errors')
    @allure.title('Create tenant setting negative(API)')
    def test_create_tenant_setting_negative(self):
        tenant_setting_payload = self.tenant_setting.to_negative_json()

        response = create_tenant_setting(tenant_setting_payload)
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("4393")
    @allure.title('Update tenant setting (API)')
    def test_update_tenant_setting(self, tenant_setting_function):
        tenant_setting_payload = self.tenant_setting.to_json

        response = update_tenant_setting(tenant_setting_function['id'], tenant_setting_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], tenant_setting_function['id'], TenantSettings.tenant_setting_id.json)
        self.assert_attr(json_response['name'], tenant_setting_function['name'], TenantSettings.name.json)
        self.assert_attr(json_response['value'], json_response['value'], TenantSettings.value.json)
        self.validate_json(json_response, self.tenant_setting.to_schema)

    @allure.id("4392")
    @allure.title('Delete tenant setting (API)')
    def test_delete_tenant_setting(self, tenant_setting_function):
        response = delete_tenant_setting(tenant_setting_function['id'])
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("4395")
    @allure.title('Get tenant setting (API)')
    def test_get_tenant_setting(self, tenant_setting_function):
        response = get_tenant_setting(tenant_setting_function['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_json(json_response, tenant_setting_function)
        self.validate_json(json_response, self.tenant_setting.to_schema)

    @allure.id("4390")
    @pytest.mark.parametrize('query', to_sort_query(tenant_setting.to_json))
    @allure.title('Query tenant settings (API)')
    def test_query_tenant_settings(self, query):
        response = get_tenant_settings_query(query)

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("4388")
    @allure.title('Check authorization for tenant settings endpoints (API)')
    @pytest.mark.parametrize('endpoint', tenant_settings_methods, ids=to_method_param)
    def test_check_authorization_for_tenant_settings_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
