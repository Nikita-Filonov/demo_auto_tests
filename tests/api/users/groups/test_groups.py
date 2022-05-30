import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.groups.groups import update_group, get_group, create_group, get_groups_query, get_groups, \
    delete_group
from base.api.users.roles.roles import get_roles
from models.users.group import Groups
from models.users.role import Roles
from models.users.role_pattern import SupportedRolePatterns
from parameters.api.users.groups import groups_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.groups
@allure.epic('Core LMS')
@allure.feature('Groups')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestGroupsApi(BaseAPI):
    group = Groups.manager

    @allure.id("432")
    @allure.title('Get groups (API)')
    def test_get_groups(self):
        response = get_groups()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.group.to_array_schema)

    @allure.id("430")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-502', name='Unable to create group')
    @allure.title('Create group (API)')
    def test_create_group(self):
        group_payload = self.group.to_json

        response = create_group(group_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_json(group_payload, json_response)
        self.validate_json(json_response, self.group.to_schema)

    @allure.id("431")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-502', name='Unable to create group')
    @allure.title('Update group (API)')
    def test_update_group(self, group_function):
        group_payload = self.group.to_json

        response = update_group(group_function['id'], group_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], group_function['id'], Groups.group_id.json)
        self.assert_attr(json_response['name'], group_payload['name'], Groups.name.json)
        self.validate_json(json_response, self.group.to_schema)

    @allure.id("4508")
    @pytest.mark.xfail(reason='Validations errors')
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-1220', name='Validations errors')
    @allure.title('Update group negative (API)')
    def test_update_group_negative(self, group_function):
        group_payload = self.group.to_negative_json()

        response = update_group(group_function['id'], group_payload)
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("424")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-502', name='Unable to create group')
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-284', name='Can not delete group')
    @allure.title('Delete group (API)')
    def test_delete_group(self, group_function):
        response = delete_group(group_function['id'])
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("420")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-502', name='Unable to create group')
    @allure.title('Get group (API)')
    def test_get_group(self, group_function):
        response = get_group(group_function['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_json(json_response, group_function)
        self.validate_json(json_response, self.group.to_schema)

    @allure.id("447")
    @pytest.mark.parametrize('query', to_sort_query(group.to_json, exclude=group.related_fields()))
    @allure.title('Query groups (API)')
    def test_query_groups(self, query):
        response = get_groups_query(query)

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("905")
    @allure.title('Check authorization for groups endpoints (API)')
    @pytest.mark.parametrize('endpoint', groups_methods, ids=to_method_param)
    def test_check_authorization_for_groups_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))

    @allure.id("4149")
    @allure.title('Crete group and check GroupOwner, GroupInstructor roles are created (API)')
    def test_group_instructor_permissions_are_created(self, group_function):
        group_roles = SupportedRolePatterns.to_list(group_function['id'])

        response = get_roles()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_any(json_response, group_roles, 'Group roles', [Roles.name.json])
