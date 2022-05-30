import allure
import pytest
from api_manager import Entities

from base.api.base import BaseAPI
from base.api.users.tenants.tenants import create_tenant, update_tenant
from models.users.tenant import Tenants
from settings import RERUNS, RERUNS_DELAY
from utils.api.validation.builders.common import build_unique_validation_message, build_null_validation_message, \
    build_max_length_validation_message


@pytest.mark.api
@pytest.mark.tenants
@allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1220', name='Validations errors')
@allure.epic('Core LMS')
@allure.feature('Tenants')
@allure.story('Validation')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.NORMAL)
class TestTenantsValidationApi(BaseAPI):
    tenant = Tenants.manager

    @allure.id("5394")
    @allure.title('Unique tenant fields validation for creation (API)')
    @pytest.mark.parametrize('fields', [[Tenants.tenant_id], [Tenants.name]])
    def test_unique_tenant_fields_validation_for_creation(self, tenant_class, fields):
        tenant = self.tenant.to_dict_with_non_unique_fields(fields=fields, payload=tenant_class)
        json_response = create_tenant(tenant).json()

        validation_message = build_unique_validation_message(fields, Entities.TENANT, tenant_class)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5391")
    @allure.title('Unique tenant fields validation for updating (API)')
    @pytest.mark.parametrize('fields', [[Tenants.name], ])
    def test_unique_tenant_fields_validation_for_updating(self, tenant_class, tenant_function, fields):
        tenant = self.tenant.to_dict_with_non_unique_fields(fields=fields, payload=tenant_class)
        json_response = update_tenant(tenant_function['id'], tenant).json()

        validation_message = build_unique_validation_message(fields, Entities.TENANT, tenant_class)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5392")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1556',
        name='[Validation][Tenant] 500 error when admin user is null'
    )
    @allure.title('Nullable tenant fields validation (API)')
    @pytest.mark.parametrize('fields', [[Tenants.name], [Tenants.admin_user]])
    def test_nullable_tenant_fields_validation(self, fields):
        tenants = self.tenant.to_dict_with_null_fields(fields=fields)
        json_response = create_tenant(tenants).json()

        validation_message = build_null_validation_message(fields)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5397")
    @allure.title('Too long tenant fields validation (API)')
    @pytest.mark.parametrize('fields', [[Tenants.name], ])
    def test_too_long_tenant_fields_validation(self, fields):
        tenant = self.tenant.to_dict_with_negative_max_length(fields=fields)
        json_response = create_tenant(tenant).json()

        validation_message = build_max_length_validation_message(fields)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)
