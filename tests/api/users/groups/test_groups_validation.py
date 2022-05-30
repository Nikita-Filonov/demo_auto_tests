import allure
import pytest
from api_manager import Entities

from base.api.base import BaseAPI
from base.api.users.groups.groups import create_group
from models.users.group import Groups
from settings import RERUNS, RERUNS_DELAY
from utils.api.validation.builders.common import build_unique_validation_message, build_null_validation_message, \
    build_max_length_validation_message


@pytest.mark.api
@pytest.mark.groups
@allure.epic('Core LMS')
@allure.feature('Groups')
@allure.story('Validation')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.NORMAL)
class TestGroupsValidationApi(BaseAPI):
    group = Groups.manager

    @allure.id("5479")
    @allure.title('Unique group fields validation (API)')
    @pytest.mark.parametrize('fields', [[Groups.group_id], ])
    def test_unique_group_fields_validation(self, group_class, fields):
        group = self.group.to_dict_with_non_unique_fields(fields=fields, payload=group_class)
        json_response = create_group(group).json()

        validation_message = build_unique_validation_message(fields, Entities.GROUP, group_class)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5478")
    @allure.title('Nullable group fields validation (API)')
    @pytest.mark.parametrize('fields', [[Groups.name], ])
    def test_nullable_group_fields_validation(self, fields):
        group = self.group.to_dict_with_null_fields(fields=fields)
        json_response = create_group(group).json()

        validation_message = build_null_validation_message(fields)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5477")
    @allure.title('Too long group fields validation (API)')
    @pytest.mark.parametrize('fields', [[Groups.name], ])
    def test_too_long_group_fields_validation(self, fields):
        group = self.group.to_dict_with_negative_max_length(fields=fields)
        json_response = create_group(group).json()

        validation_message = build_max_length_validation_message(fields)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)
