import uuid

import allure
import pytest
from alms_integration import start_objective_workflow

from base.api.base import BaseAPI
from base.api.users.objectives.objective_workflows import get_started_objective_workflows
from models.users.objective_workflow import ObjectiveWorkflowStates, ObjectiveWorkflows
from settings import RERUNS, RERUNS_DELAY


@allure.issue(
    url='https://youtrack.alemira.dev/issue/ALMS-525',
    name='Objective workflow aggregates API returns 500 error'
)
@pytest.mark.api
@pytest.mark.start_objective_workflow
@allure.epic('Core LMS')
@allure.feature('Start objective workflow')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestStartObjectiveWorkflowApi(BaseAPI):
    objective_workflow = ObjectiveWorkflows.manager

    @allure.id("543")
    @allure.title('Get started objective workflows (API)')
    def test_get_started_objective_workflow(self):
        response = get_started_objective_workflows()
        self.assert_response_status(response.status_code, self.http.OK)

    @allure.id("1776")
    @allure.title('Start objective workflow (API)')
    def test_start_objective_workflow(self, objective_workflow_aggregate):
        start_payload = {
            "id": str(uuid.uuid4()),
            "objectiveWorkflowAggregateId": objective_workflow_aggregate['id']
        }
        response = start_objective_workflow(start_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], start_payload['id'], ObjectiveWorkflows.objective_workflow_id.json)
        self.assert_attr(json_response['objectiveId'], objective_workflow_aggregate['objective']['id'],
                         ObjectiveWorkflows.objective_id.json)
        self.assert_attr(json_response['state'], ObjectiveWorkflowStates.IN_PROGRESS.value,
                         ObjectiveWorkflows.state.json)
        self.validate_json(json_response, self.objective_workflow.to_schema)

    @allure.id("549")
    @allure.title('Start objective workflow negative (API)')
    def test_start_objective_workflow_negative(self):
        start_payload = {"objectiveWorkflowAggregateId": None}
        response = start_objective_workflow(start_payload)
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)
