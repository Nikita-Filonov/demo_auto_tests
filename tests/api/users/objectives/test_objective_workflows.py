import uuid

import allure
import pytest
from alms_integration import get_objective_workflows

from base.api.base import BaseAPI
from base.api.users.objectives.objective_workflows import get_objective_workflow, get_objective_workflows_query
from models.users.objective_workflow import ObjectiveWorkflowStates, ObjectiveWorkflows
from parameters.api.users.objective_workflows import objective_workflow_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.objective_workflows import check_objective_workflow_state
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.objective_workflows
@allure.epic('Core LMS')
@allure.feature('Objective workflows')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestObjectivesWorkflowsApi(BaseAPI):
    objective_workflow = ObjectiveWorkflows.manager

    @allure.id("485")
    @allure.title('Get objective workflows (API)')
    def test_get_objective_workflows(self):
        response = get_objective_workflows()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.objective_workflow.to_array_schema)

    @allure.id("484")
    @allure.title('Get objective workflow negative (API)')
    def test_get_objective_workflow_negative(self):
        response = get_objective_workflow(uuid.uuid4())
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("1885")
    @pytest.mark.parametrize('query', to_sort_query(objective_workflow.to_json,
                                                    exclude=objective_workflow.related_fields()))
    @allure.title('Query objective workflows (API)')
    def test_query_objective_workflows(self, query):
        response = get_objective_workflows_query(query)
        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.title('Check authorization for objective workflows (API)')
    @pytest.mark.parametrize('endpoint', objective_workflow_methods, ids=to_method_param)
    def test_check_authorization_for_objective_workflows(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))

    @allure.id("4072")
    @allure.title('Check started objective workflow (API)')
    def test_check_started_objective_workflow(self, started_course_ui):
        check_objective_workflow_state(started_course_ui, ObjectiveWorkflowStates.IN_PROGRESS)

    @allure.id("4074")
    @allure.title('Check submitted objective workflow (API)')
    def test_check_submitted_objective_workflow(self, submitted_workflow_ui):
        check_objective_workflow_state(submitted_workflow_ui, ObjectiveWorkflowStates.SUBMITTED)

    @allure.id("4073")
    @allure.title('Check in grade objective workflow (API)')
    def test_check_in_grade_objective_workflow(self, in_grade_workflow_ui):
        check_objective_workflow_state(in_grade_workflow_ui, ObjectiveWorkflowStates.IN_GRADING)

    @allure.id("4075")
    @allure.title('Check grade objective workflow (API)')
    def test_check_grade_objective_workflow(self, graded_workflow_ui):
        check_objective_workflow_state(graded_workflow_ui, ObjectiveWorkflowStates.GRADED)
