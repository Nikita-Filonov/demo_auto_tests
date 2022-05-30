import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.objectives.objective_workflows import submit_objective_workflow, get_submitted_objective_workflows
from models.users.objective_workflow import ObjectiveWorkflows, ObjectiveWorkflowStates
from settings import RERUNS, RERUNS_DELAY


@allure.issue(
    url='https://youtrack.alemira.dev/issue/ALMS-525',
    name='Objective workflow aggregates API returns 500 error'
)
@pytest.mark.api
@pytest.mark.submit_objective_workflow
@allure.epic('Core LMS')
@allure.feature('Submit objective workflow')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestSubmitObjectiveWorkflowApi(BaseAPI):
    objective_workflow = ObjectiveWorkflows.manager

    @allure.id("551")
    @allure.title('Get submitted objective workflows (API)')
    def test_get_submitted_objective_workflow(self):
        response = get_submitted_objective_workflows()
        self.assert_response_status(response.status_code, self.http.OK)

    @allure.id("1777")
    @allure.title('Submit objective workflow (API)')
    def test_submit_objective_workflow(self, started_course_ui):
        workflow_id = started_course_ui[self.roles.LEARNER]['workflow_id']
        objective_id = started_course_ui[self.roles.LEARNER]['objective_id']

        response = submit_objective_workflow({'id': workflow_id})
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], workflow_id, ObjectiveWorkflows.objective_workflow_id.json)
        self.assert_attr(json_response['objectiveId'], objective_id, ObjectiveWorkflows.objective_id.json)
        self.assert_attr(json_response['state'], ObjectiveWorkflowStates.SUBMITTED.value, ObjectiveWorkflows.state.json)
        self.validate_json(json_response, self.objective_workflow.to_schema)

    @allure.id("548")
    @allure.title('Submit objective workflow negative (API)')
    def test_submit_objective_workflow_negative(self):
        response = submit_objective_workflow({"id": None})
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)
