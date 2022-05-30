import uuid

import allure
import pytest
from api_manager import Entities

from base.api.base import BaseAPI
from base.api.users.group_users.group_users import create_group_user
from models.users.group import Groups
from models.users.group_user import GroupUsers
from models.users.user import Users
from settings import RERUNS, RERUNS_DELAY
from utils.api.validation.builders.common import build_unique_validation_message, build_null_validation_message, \
    build_ref_does_not_exists_validation_message


@pytest.mark.api
@pytest.mark.groups
@allure.epic('Core LMS')
@allure.feature('Group users')
@allure.story('Validation')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.NORMAL)
class TestGroupUsersValidationApi(BaseAPI):
    group_user = GroupUsers.manager

    @allure.id("5475")
    @pytest.mark.skip(reason='[Validation][GroupUser] group_user_id is not validated for non unique field')
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1602',
        name='[Validation][GroupUser] group_user_id is not validated for non unique field'
    )
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1604',
        name='[Validation][GroupUser] Group user validation message is not correct if user already exists in group'
    )
    @allure.title('Unique group user fields validation (API)')
    @pytest.mark.parametrize('fields, keys', [
        ([GroupUsers.group_user_id], []),
        ([GroupUsers.group_id, GroupUsers.user_id], [('group', 'id'), ('user', 'id')])
    ])
    def test_unique_group_user_fields_validation(self, group_user_class, fields, keys):
        group_user = self.group_user.to_dict_with_non_unique_fields(fields=fields, payload=group_user_class, keys=keys)
        json_response = create_group_user(group_user).json()

        validation_message = build_unique_validation_message(fields, Entities.GROUP_USER, group_user_class, keys)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5476")
    @pytest.mark.skip(
        reason='[Validation][GroupUser] The JSON value could not be converted to System.Guid for groupId, userId'
    )
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1605',
        name='[Validation][GroupUser] The JSON value could not be converted to System.Guid for groupId, userId'
    )
    @allure.title('Nullable group user fields validation (API)')
    @pytest.mark.parametrize('fields', [
        [GroupUsers.user_id],
        [GroupUsers.group_id],
        [GroupUsers.group_id, GroupUsers.user_id]
    ])
    def test_nullable_group_user_fields_validation(self, fields):
        group_user = self.group_user.to_dict_with_null_fields(fields=fields)
        json_response = create_group_user(group_user).json()

        validation_message = build_null_validation_message(fields)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5474")
    @allure.title('Reference does not exists group user fields validation (API)')
    @pytest.mark.parametrize('field, entity_key, entity_name', [
        (GroupUsers.group_id.json, Groups.group_id.json, Entities.GROUP),
        (GroupUsers.user_id.json, Users.user_id.json, Entities.USER)
    ])
    def test_reference_does_not_exists_group_user_fields_validation(self, field, entity_key, entity_name):
        group_user = GroupUsers(**{field: uuid.uuid4()}).manager.to_dict()
        json_response = create_group_user(group_user).json()

        validation_message = build_ref_does_not_exists_validation_message(
            property_name=field,
            entity=Entities.GROUP_USER,
            referenced_entity_name=entity_name,
            referenced_entity_key=entity_key,
            referenced_value=group_user[field]
        )

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)
