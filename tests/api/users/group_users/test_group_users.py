import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.group_users.group_users import get_group_users, get_group_user, create_group_user, \
    get_group_users_query, delete_group_user
from models.users.group_user import GroupUsers
from parameters.api.users.group_users import group_user_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.group_users
@allure.epic('Core LMS')
@allure.feature('Group users')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestGroupUsersApi(BaseAPI):
    group_user = GroupUsers.manager

    @allure.id("536")
    @allure.title('Get group users (API)')
    def test_get_group_users(self):
        response = get_group_users()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.group_user.to_array_schema)

    @allure.id("541")
    @allure.title('Create group user (API)')
    def test_create_group_user(self):
        group_users_payload = self.group_user.to_json

        response = create_group_user(group_users_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], group_users_payload['id'], GroupUsers.group_user_id.json)
        self.assert_attr(json_response['user']['id'], group_users_payload['userId'], GroupUsers.user_id.json)
        self.assert_attr(json_response['group']['id'], group_users_payload['groupId'], GroupUsers.group_id.json)
        self.validate_json(json_response, self.group_user.to_schema)

    @allure.title('Create group user negative (API)')
    def test_create_group_user_negative(self):
        group_users_payload = self.group_user.to_negative_json()

        response = create_group_user(group_users_payload)
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("537")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-502', name='Unable to create group')
    @allure.title('Delete group user (API)')
    def test_delete_group_user(self, group_user_function):
        delete_group_user(group_user_function['id'])
        response = get_group_user(group_user_function['id'])

        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("535")
    @pytest.mark.parametrize('query', to_sort_query(group_user.to_json, exclude=group_user.related_fields()))
    @allure.title('Query group users (API)')
    def test_query_group_users(self, query):
        response = get_group_users_query(query)
        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("534")
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-502', name='Unable to create group')
    @allure.title('Get group user (API)')
    def test_get_group_user(self, group_user_function):
        response = get_group_user(group_user_function['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_json(json_response, group_user_function)

    @allure.id("908")
    @allure.title('Check authorization for group users endpoints (API)')
    @pytest.mark.parametrize('endpoint', group_user_methods, ids=to_method_param)
    def test_check_authorization_for_group_users_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
