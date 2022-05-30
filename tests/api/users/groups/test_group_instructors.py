import allure
import pytest
from alms_integration import get_objective_workflows

from base.api.users.group_users.group_users import get_group_users
from base.api.users.groups.base_groups import GroupsBaseAPI
from base.api.users.groups.groups import get_groups
from base.api.users.objectives.objectives import get_objective_resource_link
from base.api.users.users.users import get_user_permissions
from base.api.ztool.launch import get_launch
from base.api.ztool.workflows import grade_workflow, get_workflow
from models.users.objective_workflow import ObjectiveWorkflows
from models.users.role import SupportedRoles
from models.users.role_pattern import SupportedRolePatterns
from models.ztool.answer import Answers
from models.ztool.workflow import Workflows, WorkflowStates
from parameters.courses.ui.ztool.answers import answers_properties
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.api.users.groups import GroupsStory
from utils.api.ztool.workflows import check_workflow_state


@pytest.mark.api
@pytest.mark.group_instructors
@allure.epic('Core LMS')
@allure.feature('Groups')
@allure.story(GroupsStory.GROUP_INSTRUCTOR.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestGroupInstructorsApi(GroupsBaseAPI):
    workflow = Workflows.manager
    objective_workflow = ObjectiveWorkflows.manager

    @allure.id("4147")
    @allure.title('Add instructor to a group and check permissions (API)')
    def test_add_instructor_to_a_group_and_check_permissions(self, group_instructor):
        instructor_scope = SupportedRolePatterns.to_group_instructor_scope(group_instructor['group']['id'])
        permissions = get_user_permissions(user=group_instructor['instructor']).json()

        self.assert_any(permissions, instructor_scope, 'Group instructor permissions', self.scope_keys)

    @allure.id("4148")
    @allure.title('The instructor can only see his group (API)')
    def test_the_instructor_can_only_see_his_group(self, group_instructor):
        groups = get_groups(user=group_instructor['instructor']).json()
        self.assert_all(groups, [group_instructor['group']], 'Groups', self.group_keys)

    @allure.id("4146")
    @allure.title('The instructor can see the users of the group (API)')
    def test_the_instructor_can_see_the_users_of_the_group(self, group_instructor):
        response = get_group_users(user=group_instructor['instructor'])
        self.assert_response_status(response.status_code, self.http.OK)

    @allure.id("4143")
    @allure.title('The instructor can see objective workflows of the group (API)')
    def test_the_instructor_can_see_objective_workflows_of_the_group(self, group_instructor):
        response = get_objective_workflows(user=group_instructor['instructor'])
        self.assert_response_status(response.status_code, self.http.OK)

    @allure.id("4144")
    @allure.title('The instructor can grade workflow of the group user (API)')
    def test_the_instructor_can_grade_workflow_of_the_group_user(self, group_instructor, in_grade_workflow_ui):
        user = group_instructor['instructor']
        workflow_id = in_grade_workflow_ui[self.roles.LEARNER]['workflow_id']
        objective_id = in_grade_workflow_ui[self.roles.LEARNER]['objective_id']
        element_id = in_grade_workflow_ui[self.roles.LEARNER]['element_id']
        launch = get_launch(SupportedRoles.INSTRUCTOR, element_id, workflow_id, objective_id, user)

        answers = Answers.manager.filter(workflow_id=workflow_id, as_json=False)
        for answer, grade in zip(answers, answers_properties):
            answer.manager.update(**grade)

        workflow_payload = self.workflow.to_json
        grade_response = grade_workflow(launch['request_id'], workflow_id, workflow_payload, user)
        workflow_response = get_workflow(launch['request_id'], workflow_id, user)

        self.assert_response_status(grade_response.status_code, self.http.OK)
        check_workflow_state(workflow_response, launch, WorkflowStates.GRADED)

    @allure.id("4213")
    @allure.title('The instructor can not grade workflow of users from another group (API)')
    def test_the_instructor_can_not_grade_workflow_of_users_from_another_group(self, group_instructor_without_user,
                                                                               in_grade_workflow_ui):
        user = group_instructor_without_user['instructor']
        workflow_id = in_grade_workflow_ui[self.roles.LEARNER]['workflow_id']
        objective_id = in_grade_workflow_ui[self.roles.LEARNER]['objective_id']
        response = get_objective_resource_link(objective_id, SupportedRoles.INSTRUCTOR.value, workflow_id, user)
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)
