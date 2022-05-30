import allure
import pytest

from base.api.users.group_users.group_users import create_group_user, delete_group_user, get_group_user
from base.api.users.groups.base_groups import GroupsBaseAPI
from base.api.users.groups.groups import get_groups, update_group, get_group, delete_group
from base.api.users.user_roles.user_roles import create_user_role, delete_user_role, get_user_role
from base.api.users.users.users import get_user_permissions
from models.users.group import Groups
from models.users.group_user import GroupUsers
from models.users.role_pattern import SupportedRolePatterns
from models.users.user_role import UserRoles
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.api.users.groups import GroupsStory


@pytest.mark.api
@pytest.mark.group_owners
@allure.epic('Core LMS')
@allure.feature('Groups')
@allure.story(GroupsStory.GROUP_OWNER.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestGroupOwnersApi(GroupsBaseAPI):
    group_user = GroupUsers.manager
    user_role = UserRoles.manager

    @allure.id("4142")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-965',
        name='The user is not always the owner of the group'
    )
    @allure.title('Create group and check that I am owner (API)')
    def test_create_group_and_check_that_i_am_owner(self, group_function):
        owner_scope = SupportedRolePatterns.to_group_owner_scope(group_function['id'])
        response = get_user_permissions()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_any(json_response, owner_scope, 'Group owner permissions', self.scope_keys)

    @allure.id("4145")
    @allure.title('The owner can see only his group in groups list (API)')
    def test_the_owner_can_see_only_his_group_in_groups_list(self, group_owner):
        response = get_groups(user=group_owner['owner'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_all(json_response, [group_owner['group']], 'Groups', self.group_keys)

    @allure.id("4141")
    @allure.title('The owner can see his group (API)')
    def test_the_owner_can_see_his_group(self, group_owner):
        response = get_group(group_owner['group']['id'], user=group_owner['owner'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_json(json_response, group_owner['group'])
        self.validate_json(json_response, self.group.to_schema)

    @allure.id("4210")
    @allure.title('The owner can not see another group (API)')
    def test_the_owner_can_not_see_another_group(self, group_owner, group_function):
        response = get_group(group_function['id'], user=group_owner['owner'])
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("4150")
    @allure.title('The owner can edit his group (API)')
    def test_the_owner_can_edit_his_group(self, group_owner):
        group_id = group_owner['group']['id']
        group_payload = self.group.to_json

        response = update_group(group_id, group_payload, user=group_owner['owner'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], group_id, Groups.group_id.json)
        self.assert_attr(json_response['name'], group_payload['name'], Groups.name.json)
        self.validate_json(json_response, self.group.to_schema)

    @allure.id("4209")
    @allure.title('The owner can not edit another group (API)')
    def test_the_owner_can_not_edit_another_group(self, group_owner, group_function):
        group_payload = self.group.to_json
        response = update_group(group_function['id'], group_payload, user=group_owner['owner'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['completed']['state'], self.state.FAILED.value, 'Response state')

    @allure.id("4151")
    @allure.title('The owner can not delete his group (API)')
    def test_the_owner_can_not_delete_his_group(self, group_owner):
        response = delete_group(group_owner['group']['id'], user=group_owner['owner'])
        self.assert_response_status(response.status_code, self.http.FORBIDDEN)

    @allure.id("4206")
    @allure.title('The owner can not delete another group (API)')
    def test_the_owner_can_not_delete_another_group(self, group_owner, group_function):
        response = delete_group(group_function['id'], user=group_owner['owner'])
        self.assert_response_status(response.status_code, self.http.FORBIDDEN)

    @allure.id("4205")
    @allure.title('The owner can add user to his group (API)')
    def test_owner_can_add_user_to_his_group(self, group_owner, user_function):
        group_user_payload = {
            GroupUsers.group_id.json: group_owner['group']['id'],
            GroupUsers.user_id.json: user_function['id']
        }
        response = create_group_user(group_user_payload, user=group_owner['owner'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(group_user_payload['groupId'], json_response['group']['id'], GroupUsers.group_id.json)
        self.assert_attr(group_user_payload['userId'], json_response['user']['id'], GroupUsers.user_id.json)
        self.validate_json(json_response, self.group_user.to_schema)

    @allure.id("4208")
    @allure.title('The owner can delete user from his group (API)')
    def test_owner_can_delete_user_from_his_group(self, group_owner):
        delete_group_user(group_owner['user']['id'], user=group_owner['owner'])
        response = get_group_user(group_owner['user']['id'])
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("4212")
    @allure.title('The owner can delete instructor from his group (API)')
    def test_owner_can_delete_instructor_from_his_group(self, group_owner, group_instructor):
        delete_user_role(group_instructor['instructor_role']['id'], user=group_owner['owner'])
        response = get_user_role(group_instructor['instructor_role']['id'])
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("4207")
    @allure.title('The owner can delete owner from his group (API)')
    def test_owner_can_delete_owner_from_his_group(self, group_owner, group_instructor):
        delete_user_role(group_owner['owner_role']['id'], user=group_owner['owner'])
        response = get_user_role(group_owner['owner_role']['id'])
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("4211")
    @pytest.mark.parametrize('role', [
        {'get_name': SupportedRolePatterns.get_instructor_role, 'name': SupportedRolePatterns.GROUP_INSTRUCTOR},
        {'get_name': SupportedRolePatterns.get_owner_role, 'name': SupportedRolePatterns.GROUP_OWNER}
    ])
    def test_the_owner_can_add_role_to_his_group(self, group_owner, role, user_function):
        allure.dynamic.title(f'The owner can add {role["name"].value} to his group (API)')
        group_instructor_payload = {
            'roleName': role['get_name'](group_owner['group']['id']),
            UserRoles.user_id.json: user_function['id']
        }
        response = create_user_role(group_instructor_payload, user=group_owner['owner'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(group_instructor_payload['roleName'], json_response['role']['name'], 'Role name')
        self.assert_attr(group_instructor_payload['userId'], json_response['user']['id'], UserRoles.user_id.json)
        self.validate_json(json_response, self.user_role.to_schema)
