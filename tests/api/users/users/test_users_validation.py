import uuid

import allure
import pytest
from api_manager import Entities

from base.api.base import BaseAPI
from base.api.users.users.users import create_user
from models.users.tenant import Tenants
from models.users.user import Users
from settings import RERUNS, RERUNS_DELAY
from utils.api.validation.builders.common import build_unique_validation_message, build_null_validation_message, \
    build_max_length_validation_message, build_ref_does_not_exists_validation_message


@pytest.mark.api
@pytest.mark.users
@allure.epic('Core LMS')
@allure.feature('Users')
@allure.story('Validation')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.NORMAL)
class TestUsersValidationApi(BaseAPI):
    user = Users.manager

    @allure.id("5377")
    @allure.title('Unique user fields validation (API)')
    @pytest.mark.parametrize('fields', [[Users.user_id], [Users.username]])
    def test_unique_user_fields_validation(self, user_class, fields):
        user = self.user.to_dict_with_non_unique_fields(fields=fields, payload=user_class)
        json_response = create_user(user).json()

        validation_message = build_unique_validation_message(fields, Entities.USER, user_class)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5378")
    @pytest.mark.skip(reason='Investigate how we should validate not nullable fields')
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1540',
        name='[Validation] Investigate how we should validate not nullable fields'
    )
    @allure.title('Nullable user fields validation (API)')
    @pytest.mark.parametrize('fields', [
        [Users.email, Users.username],
    ])
    def test_nullable_user_fields_validation(self, fields):
        user = self.user.to_dict_with_null_fields(fields=fields)
        json_response = create_user(user).json()

        validation_message = build_null_validation_message(fields)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5386")
    @pytest.mark.skip(reason='[Validation][Objective][Activity] Tenant id reference is not validated')
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1547',
        name='[Validation][Objective][Activity] Tenant id reference is not validated'
    )
    @allure.title('Reference does not exists user fields validation (API)')
    @pytest.mark.parametrize('field, entity_key, entity_name', [
        (Users.tenant_id.json, Tenants.tenant_id.json, Entities.TENANT)
    ])
    def test_reference_does_not_exists_user_fields_validation(self, field, entity_key, entity_name):
        user = Users(**{field: uuid.uuid4()}).manager.to_dict()
        json_response = create_user(user).json()

        validation_message = build_ref_does_not_exists_validation_message(
            property_name=field,
            entity=Entities.USER,
            referenced_entity_name=entity_name,
            referenced_entity_key=entity_key,
            referenced_value=user[field]
        )

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5375")
    @allure.title('Too long user fields validation (API)')
    @pytest.mark.parametrize('fields', [
        [Users.email],
        [Users.email, Users.username],
        [Users.email, Users.last_name],
        [Users.username],
        [Users.first_name, Users.email],
        [Users.middle_name, Users.username],
        [Users.external_id]
    ])
    def test_too_long_user_fields_validation(self, fields):
        user = self.user.to_dict_with_negative_max_length(fields=fields)
        json_response = create_user(user).json()

        validation_message = build_max_length_validation_message(fields)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)
