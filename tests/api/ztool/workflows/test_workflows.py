from datetime import datetime, timedelta

import allure
import pytest

from base.api.base import BaseAPI
from base.api.ztool.launch import get_launch
from base.api.ztool.workflows import get_workflow, submit_workflow, send_submitted_workflow_to_grading, \
    get_workflow_answers, grade_workflow, approve_workflow, send_approved_workflow_to_finished
from models.users.role import SupportedRoles
from models.ztool.answer import Answers
from models.ztool.workflow import Workflows, WorkflowStates
from settings import RERUNS, RERUNS_DELAY
from tests.api.ztool.conftest import ROLES
from utils.api.ztool.workflows import check_workflow_state


@pytest.mark.api
@pytest.mark.workflows
@allure.epic('Core LMS')
@allure.feature('Workflows')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestWorkflowsApi(BaseAPI):
    workflow = Workflows.manager

    ROLES_CAN_READ_ANSWERS = [SupportedRoles.LEARNER, SupportedRoles.AUTHOR, SupportedRoles.INSTRUCTOR]

    @allure.id("1944")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1107',
        name='204 response code on GET to /api/v1/objectives/{id}/objective-workflow-aggregate'
    )
    @allure.title('Get workflow (API)')
    def test_get_workflow(self, learner):
        request_id = learner['request_id']
        workflow_id = learner['workflow_id']
        response = get_workflow(request_id, workflow_id)

        check_workflow_state(response, learner, WorkflowStates.IN_PROGRESS)

    @allure.id("1946")
    @allure.title('Get workflow answers (API)')
    @pytest.mark.parametrize('launch', ROLES_CAN_READ_ANSWERS, indirect=['launch'])
    def test_get_workflow_answers(self, launch: dict):
        response = get_workflow_answers(launch['request_id'], launch['workflow_id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, Answers.manager.to_array_schema)

    @allure.id("1941")
    @allure.title('Submit workflow (API)')
    def test_submit_workflow(self, learner):
        request_id = learner['request_id']
        workflow_id = learner['workflow_id']

        submit_response = submit_workflow(request_id, workflow_id)
        workflow_response = get_workflow(request_id, workflow_id)

        self.assert_response_status(submit_response.status_code, self.http.OK)
        check_workflow_state(workflow_response, learner, WorkflowStates.SUBMITTED)

    @allure.id("1940")
    @allure.title('Submit workflow second time (API)')
    def test_submit_workflow_second_time(self, submitted_workflow):
        request_id = submitted_workflow[self.roles.LEARNER]['request_id']
        workflow_id = submitted_workflow[self.roles.LEARNER]['workflow_id']

        submit_response = submit_workflow(request_id, workflow_id)
        submit_json_response = submit_response.json()

        workflow_response = get_workflow(request_id, workflow_id)

        self.assert_response_status(submit_response.status_code, self.http.FORBIDDEN)
        self.assert_json(submit_json_response, {'error': 'Insufficient role permissions for submitting'})
        check_workflow_state(workflow_response, submitted_workflow[self.roles.LEARNER], WorkflowStates.SUBMITTED)

    @allure.id("1943")
    @allure.title('Send submitted workflow to grading (API)')
    def test_send_submitted_workflow_to_grading(self, submitted_workflow, author):
        request_id = submitted_workflow[self.roles.LEARNER]['request_id']
        workflow_id = submitted_workflow[self.roles.LEARNER]['workflow_id']

        in_grading_response = send_submitted_workflow_to_grading(author['request_id'])
        workflow_response = get_workflow(request_id, workflow_id)

        self.assert_response_status(in_grading_response.status_code, self.http.OK)
        check_workflow_state(workflow_response, submitted_workflow[self.roles.LEARNER], WorkflowStates.IN_GRADING)

    @allure.id("4083")
    @allure.title('Send approved workflow to finished state (API)')
    def test_send_approved_workflow_to_finished_state(self, approved_workflow, author):
        request_id = approved_workflow[self.roles.LEARNER]['request_id']
        workflow_id = approved_workflow[self.roles.LEARNER]['workflow_id']

        in_grading_response = send_approved_workflow_to_finished(approved_workflow[self.roles.AUTHOR]['request_id'])
        workflow_response = get_workflow(request_id, workflow_id)

        self.assert_response_status(in_grading_response.status_code, self.http.OK)
        check_workflow_state(workflow_response, approved_workflow[self.roles.LEARNER], WorkflowStates.FINISHED)

    @allure.id("1942")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-755',
        name='500 error when grading workflow'
    )
    @allure.title('Grade workflow (API)')
    def test_grade_workflow(self, in_grade_workflow, instructor):
        request_id = in_grade_workflow[self.roles.LEARNER]['request_id']
        workflow_id = in_grade_workflow[self.roles.LEARNER]['workflow_id']
        payload = self.workflow.to_json

        grade_response = grade_workflow(instructor['request_id'], workflow_id, payload)
        workflow_response = get_workflow(request_id, workflow_id)

        self.assert_response_status(grade_response.status_code, self.http.OK)
        check_workflow_state(workflow_response, in_grade_workflow[self.roles.LEARNER], WorkflowStates.GRADED, payload)

    @allure.id("4051")
    @allure.title('Approve workflow (API)')
    def test_approve_workflow(self, graded_workflow, observer):
        request_id = graded_workflow[self.roles.LEARNER]['request_id']
        workflow_id = graded_workflow[self.roles.LEARNER]['workflow_id']

        approve_response = approve_workflow(observer['request_id'], workflow_id)
        workflow_response = get_workflow(request_id, workflow_id)

        self.assert_response_status(approve_response.status_code, self.http.OK)
        check_workflow_state(workflow_response, graded_workflow[self.roles.LEARNER], WorkflowStates.GRADING_APPROVED)

    @allure.id("4050")
    @allure.title('Roles can not approve workflow [negative] (API)')
    @pytest.mark.parametrize('role', ROLES)
    def test_roles_can_not_approve_workflow_negative(self, graded_workflow, role):
        element_id = graded_workflow[self.roles.LEARNER]['element_id']
        workflow_id = graded_workflow[self.roles.LEARNER]['workflow_id']
        objective_id = graded_workflow[self.roles.LEARNER]['objective_id']
        launch = get_launch(role, element_id, workflow_id, objective_id)

        approve_response = approve_workflow(launch['request_id'], workflow_id)
        approve_json_response = approve_response.json()

        self.assert_response_status(approve_response.status_code, self.http.FORBIDDEN)
        self.assert_json(approve_json_response, {"error": "Insufficient role permissions for grading"})

    @allure.id("1947")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-755',
        name='500 error when grading workflow'
    )
    @allure.title('Grade workflow second time (API)')
    def test_grade_workflow_second_time(self, graded_workflow):
        request_id = graded_workflow[self.roles.INSTRUCTOR]['request_id']
        workflow_id = graded_workflow[self.roles.INSTRUCTOR]['workflow_id']
        payload = self.workflow.to_json

        grade_response = grade_workflow(request_id, workflow_id, payload)

        workflow_response = get_workflow(request_id, workflow_id)
        workflow_json_response = workflow_response.json()

        self.assert_response_status(grade_response.status_code, self.http.FORBIDDEN)
        check_workflow_state(workflow_response, graded_workflow[self.roles.INSTRUCTOR], WorkflowStates.GRADED)
        self.assert_attr(workflow_json_response['feedback'], graded_workflow['data']['feedback'],
                         Workflows.feedback.json)

    @allure.id("1945")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-755',
        name='500 error when grading workflow'
    )
    @allure.title('Grade workflow from passed time (API)')
    @pytest.mark.parametrize(
        'learner',
        [
            {
                'element':
                    {
                        'grading_end_date': datetime.now() - timedelta(days=5),
                        'grading_start_date': datetime.now() - timedelta(days=10),
                        'grade_disclosure_date': datetime.now() - timedelta(days=3)
                    }
            },
            {
                'element':
                    {
                        'grading_end_date': datetime.now() - timedelta(days=2),
                        'grading_start_date': datetime.now() - timedelta(days=5),
                        'grade_disclosure_date': datetime.now() - timedelta(days=1)
                    }
            }
        ],
        indirect=['learner']
    )
    def test_grade_workflow_from_passed_time(self, in_grade_workflow, instructor, learner):
        request_id = instructor['request_id']
        workflow_id = instructor['workflow_id']
        payload = self.workflow.to_json

        grade_response = grade_workflow(request_id, workflow_id, payload)
        workflow_response = get_workflow(request_id, workflow_id)

        self.assert_response_status(grade_response.status_code, self.http.OK)
        check_workflow_state(workflow_response, in_grade_workflow[self.roles.LEARNER], WorkflowStates.GRADED, payload)
