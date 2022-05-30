import uuid

import allure
import pytest
from alms_integration import create_activity
from api_manager import Entities

from base.api.base import BaseAPI
from models.users.activity import Activities
from models.users.tenant import Tenants
from settings import RERUNS, RERUNS_DELAY
from utils.api.validation.builders.common import build_unique_validation_message, build_null_validation_message, \
    build_max_length_validation_message, build_ref_does_not_exists_validation_message


@allure.issue(
    name='Wrong error validation message for Activity.Code field',
    url='https://youtrack.alemira.dev/issue/ALMS-1208'
)
@pytest.mark.api
@pytest.mark.activities
@allure.epic('Core LMS')
@allure.feature('Activities')
@allure.story('Validation')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.NORMAL)
class TestActivitiesValidationApi(BaseAPI):
    activity = Activities.manager

    @allure.id("5367")
    @allure.title('Unique activity fields validation (API)')
    @pytest.mark.parametrize('fields', [[Activities.activity_id], [Activities.code]])
    def test_unique_activity_fields_validation(self, activity_class, fields):
        _, activity = activity_class

        activity = self.activity.to_dict_with_non_unique_fields(fields=fields, payload=activity)
        json_response = create_activity(activity).json()

        validation_message = build_unique_validation_message(fields, Entities.ACTIVITY, activity)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5365")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1489',
        name='[Validation][Activity] Validation message is not correct when tenantId is null'
    )
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1490',
        name='[Validation][Activity] Validation message is not correct when type is null'
    )
    @allure.title('Nullable activity fields validation (API)')
    @pytest.mark.parametrize('fields', [
        [Activities.name],
        [Activities.code],
        [Activities.type],
        [Activities.tenant_id]
    ])
    def test_nullable_activity_fields_validation(self, fields):
        activity = self.activity.to_dict_with_null_fields(fields=fields)
        json_response = create_activity(activity).json()

        validation_message = build_null_validation_message(fields)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5389")
    @pytest.mark.skip(reason='[Validation][Objective][Activity] Tenant id reference is not validated')
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1547',
        name='[Validation][Objective][Activity] Tenant id reference is not validated'
    )
    @allure.title('Reference does not exists activity fields validation (API)')
    @pytest.mark.parametrize('field, entity_key, entity_name', [
        (Activities.tenant_id.json, Tenants.tenant_id.json, Entities.TENANT)
    ])
    def test_reference_does_not_exists_activity_fields_validation(self, field, entity_key, entity_name):
        activity = Activities(**{field: uuid.uuid4()}).manager.to_json
        json_response = create_activity(activity).json()

        validation_message = build_ref_does_not_exists_validation_message(
            property_name=field,
            entity=Entities.ACTIVITY,
            referenced_entity_name=entity_name,
            referenced_entity_key=entity_key,
            referenced_value=activity[field]
        )

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5366")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1498',
        name='[Validation][Activity] Duplicated validation message for "toolUrl", "toolResourceId"'
    )
    @allure.title('Too long activity fields validation (API)')
    @pytest.mark.parametrize('fields', [
        [Activities.name],
        [Activities.code],
        [Activities.name, Activities.code],
        [Activities.name, Activities.code, Activities.description],
        [Activities.tool_url, Activities.editor_content],
        [Activities.tool_resource_id, Activities.editor_content]
    ])
    def test_too_long_activity_fields_validation(self, fields):
        activity = self.activity.to_dict_with_negative_max_length(fields=fields)
        json_response = create_activity(activity).json()

        validation_message = build_max_length_validation_message(fields)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)
