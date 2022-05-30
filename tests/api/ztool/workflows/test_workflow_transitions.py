import allure
import pytest

from base.api.base import BaseAPI
from base.api.ztool.workflows import undo_submit_workflow, get_workflow, undo_grade_workflow, \
    revoke_in_grading_workflow_to_progress
from models.users.role import SupportedRoles
from models.ztool.workflow import WorkflowStates
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.api.ztool.workflows import WorkflowsStory
from utils.api.ztool.workflows import check_workflow_state


@pytest.mark.api
@pytest.mark.workflow_transitions
@allure.epic('Core LMS')
@allure.feature('Workflows')
@allure.story(WorkflowsStory.WORKFLOW_TRANSITIONS.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestWorkflowTransitionsApi(BaseAPI):

    @allure.id("4220")
    @allure.title('Undo submit workflow (API)')
    @pytest.mark.parametrize('role', [SupportedRoles.LEARNER, SupportedRoles.OBSERVER])
    def test_undo_submit_workflow(self, submitted_workflow, role):
        request_id = submitted_workflow[role]['request_id']
        workflow_id = submitted_workflow[role]['workflow_id']

        undo_response = undo_submit_workflow(request_id, workflow_id)
        workflow_response = get_workflow(request_id, workflow_id)

        self.assert_response_status(undo_response.status_code, self.http.OK)
        check_workflow_state(workflow_response, submitted_workflow[role], WorkflowStates.IN_PROGRESS)

    @allure.id("4310")
    @allure.title('Undo submit workflow negative (API)')
    @pytest.mark.parametrize('role', [SupportedRoles.INSTRUCTOR, SupportedRoles.AUTHOR])
    def test_undo_submit_workflow_negative(self, submitted_workflow, role):
        request_id = submitted_workflow[role]['request_id']
        workflow_id = submitted_workflow[role]['workflow_id']

        undo_response = undo_submit_workflow(request_id, workflow_id)
        self.assert_response_status(undo_response.status_code, self.http.FORBIDDEN)

    @allure.id("4243")
    @allure.title('Undo grade workflow (API)')
    @pytest.mark.parametrize('role', [SupportedRoles.INSTRUCTOR, SupportedRoles.OBSERVER])
    def test_undo_grade_workflow(self, graded_workflow, role):
        request_id = graded_workflow[role]['request_id']
        workflow_id = graded_workflow[role]['workflow_id']

        undo_response = undo_grade_workflow(request_id, workflow_id)
        workflow_response = get_workflow(request_id, workflow_id)

        self.assert_response_status(undo_response.status_code, self.http.OK)
        check_workflow_state(workflow_response, graded_workflow[role], WorkflowStates.IN_GRADING)

    @allure.id("4309")
    @allure.title('Undo grade workflow negative (API)')
    @pytest.mark.parametrize('role', [SupportedRoles.LEARNER, SupportedRoles.AUTHOR])
    def test_undo_grade_workflow_negative(self, graded_workflow, role):
        request_id = graded_workflow[role]['request_id']
        workflow_id = graded_workflow[role]['workflow_id']

        undo_response = undo_grade_workflow(request_id, workflow_id)
        self.assert_response_status(undo_response.status_code, self.http.FORBIDDEN)

    @allure.id("4308")
    @allure.title('Revoke in grading to progress (API)')
    @pytest.mark.parametrize('role', [SupportedRoles.OBSERVER])
    def test_revoke_in_grading_to_progress(self, in_grade_workflow, role):
        request_id = in_grade_workflow[role]['request_id']
        workflow_id = in_grade_workflow[role]['workflow_id']

        undo_response = revoke_in_grading_workflow_to_progress(request_id, workflow_id)
        workflow_response = get_workflow(request_id, workflow_id)

        self.assert_response_status(undo_response.status_code, self.http.OK)
        check_workflow_state(workflow_response, in_grade_workflow[role], WorkflowStates.IN_PROGRESS)

    @allure.id("4311")
    @allure.title('Revoke in grading to progress negative (API)')
    @pytest.mark.parametrize('role', [SupportedRoles.LEARNER, SupportedRoles.AUTHOR, SupportedRoles.INSTRUCTOR])
    def test_revoke_in_grading_to_progress_negative(self, in_grade_workflow, role):
        request_id = in_grade_workflow[role]['request_id']
        workflow_id = in_grade_workflow[role]['workflow_id']

        undo_response = revoke_in_grading_workflow_to_progress(request_id, workflow_id)
        self.assert_response_status(undo_response.status_code, self.http.FORBIDDEN)
