import uuid

import allure
import pytest
from alms_integration import create_objective
from api_manager import Entities

from base.api.base import BaseAPI
from models.users.activity import Activities
from models.users.objective import Objectives
from settings import RERUNS, RERUNS_DELAY
from utils.api.validation.builders.common import build_unique_validation_message, \
    build_ref_does_not_exists_validation_message, build_max_length_validation_message, build_null_validation_message


@pytest.mark.api
@pytest.mark.objectives
@allure.epic('Core LMS')
@allure.feature('Objectives')
@allure.story('Validation')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.NORMAL)
class TestObjectivesValidationApi(BaseAPI):
    objective = Objectives.manager

    @allure.id("5384")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1545',
        name='[Validation][Objective] Code is not unique field for Objective'
    )
    @allure.title('Unique objective fields validation (API)')
    @pytest.mark.parametrize('fields', [[Objectives.objective_id], [Objectives.code]])
    def test_unique_objective_fields_validation(self, objective_class, fields):
        objective = self.objective.to_dict_with_non_unique_fields(fields=fields, payload=objective_class)
        json_response = create_objective(objective).json()

        validation_message = build_unique_validation_message(fields, Entities.OBJECTIVE, objective_class)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5387")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1547',
        name='[Validation][Objective][Activity] Tenant id reference is not validated'
    )
    @allure.title('Reference does not exists objective fields validation (API)')
    @pytest.mark.parametrize('field, entity_key, entity_name', [
        (Objectives.activity_id.json, Activities.activity_id.json, Entities.ACTIVITY),
    ])
    def test_reference_does_not_exists_objective_fields_validation(self, field, entity_key, entity_name):
        objective = Objectives(**{field: uuid.uuid4()}).manager.to_dict()
        json_response = create_objective(objective).json()

        validation_message = build_ref_does_not_exists_validation_message(
            property_name=field,
            entity=Entities.OBJECTIVE,
            referenced_entity_name=entity_name,
            referenced_entity_key=entity_key,
            referenced_value=objective[field]
        )

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5388")
    @pytest.mark.skip(reason='Investigate how we should validate not nullable fields')
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1540',
        name='[Validation] Investigate how we should validate not nullable fields'
    )
    @allure.title('Nullable objective fields validation (API)')
    @pytest.mark.parametrize('fields', [
        [Objectives.name],
        [Objectives.code],
        [Objectives.description],
        [Objectives.tenant_id],
        [Objectives.activity_id],
    ])
    def test_nullable_objective_fields_validation(self, fields):
        objectives = self.objective.to_dict_with_null_fields(fields=fields)
        json_response = create_objective(objectives).json()

        validation_message = build_null_validation_message(fields)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)

    @allure.id("5385")
    @allure.title('Too long objective fields validation (API)')
    @pytest.mark.parametrize('fields', [
        [Objectives.name],
        [Objectives.code],
        [Objectives.name, Objectives.code],
        [Objectives.name, Objectives.code, Objectives.description],
        [Objectives.description]
    ])
    def test_too_long_objective_fields_validation(self, fields):
        objective = self.objective.to_dict_with_negative_max_length(fields=fields)
        json_response = create_objective(objective).json()

        validation_message = build_max_length_validation_message(fields)

        self.assert_json(self.get_validation_result(json_response), validation_message)
        self.validate_json(json_response, self.validation_result_model.manager.to_schema)
