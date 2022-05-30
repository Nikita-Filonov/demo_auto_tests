import allure
import pytest
from api_manager import Entities

from base.api.base import BaseAPI
from base.api.users.tenant_settings.tenant_settings import create_tenant_setting
from models.users.tenant_setting import TenantSettings
from settings import RERUNS, RERUNS_DELAY
from utils.api.validation.builders.common import build_unique_validation_message, build_null_validation_message, \
    build_max_length_validation_message


@pytest.mark.api
@pytest.mark.tenant_settings
@allure.epic('Core LMS')
@allure.feature('Tenant settings')
@allure.story('Validation')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.NORMAL)
class TestTenantSettingsValidationApi(BaseAPI):
    tenant_settings = TenantSettings.manager

    @allure.id("5446")
    @allure.title('Unique tenant setting fields validation for creation (API)')
    @pytest.mark.parametrize('fields', [
        [TenantSettings.name],
        [TenantSettings.tenant_setting_id],
        [TenantSettings.tenant_setting_id, TenantSettings.name],
    ])
    def test_unique_tenant_setting_fields_validation_for_creation(self, tenant_setting_class, fields):
        tenant_setting = self.tenant_settings.to_dict_with_non_unique_fields(
            fields=fields, payload=tenant_setting_class)
        json_response = create_tenant_setting(tenant_setting).json()

        validation_message = build_unique_validation_message(fields, Entities.TENANT_SETTING, tenant_setting_class)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5448")
    @allure.title('Nullable tenant setting fields validation (API)')
    @pytest.mark.parametrize('fields', [[TenantSettings.name], ])
    def test_nullable_tenant_setting_fields_validation(self, fields):
        tenant_settings = self.tenant_settings.to_dict_with_null_fields(fields=fields)
        json_response = create_tenant_setting(tenant_settings).json()

        validation_message = build_null_validation_message(fields)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5447")
    @allure.title('Too long tenant setting fields validation (API)')
    @pytest.mark.parametrize('fields', [[TenantSettings.name], ])
    def test_too_long_tenant_setting_fields_validation(self, fields):
        tenant_setting = self.tenant_settings.to_dict_with_negative_max_length(fields=fields)
        json_response = create_tenant_setting(tenant_setting).json()

        validation_message = build_max_length_validation_message(fields)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)
