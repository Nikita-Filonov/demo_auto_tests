import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.lms_users.lms_users import get_lms_users, create_lms_user, get_lms_user, update_lms_user, \
    get_lms_users_query
from models.users.lms_user import LmsUsers
from parameters.api.users.lms_users import lms_users_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.lms_users
@allure.epic('Core LMS')
@allure.feature('Lms Users')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestUsersApi(BaseAPI):
    lms_user = LmsUsers.manager

    @allure.id("3889")
    @allure.title('Get lms users (API)')
    def test_get_lms_users(self):
        response = get_lms_users()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.lms_user.to_array_schema)

    @allure.id("3891")
    @allure.title('Create lms user (API)')
    def test_create_lms_user(self):
        payload = self.lms_user.to_json

        response = create_lms_user(payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], payload['id'], LmsUsers.user_id.json)
        self.assert_attr(json_response['username'], payload['username'], LmsUsers.username.json)
        self.assert_attr(json_response['email'], payload['email'], LmsUsers.email.json)
        self.assert_attr(json_response['details'], payload['details'], LmsUsers.details.json)
        self.validate_json(json_response, self.lms_user.to_schema)

    @allure.id("3892")
    @pytest.mark.xfail(reason='Unable to update "LmsUsers"')
    @allure.issue(url='https://youtrack.alemira.dev/issue/ALMS-788', name='Unable to update "LmsUsers"')
    @allure.title('Update lms user (API)')
    def test_update_lms_user(self, lms_user):
        update_payload = self.lms_user.to_json

        response = update_lms_user(lms_user['id'], update_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], lms_user['id'], LmsUsers.user_id.json)
        self.assert_attr(json_response['username'], update_payload['username'], LmsUsers.username.json)
        self.assert_attr(json_response['email'], update_payload['email'], LmsUsers.email.json)
        self.assert_attr(json_response['details'], update_payload['details'], LmsUsers.details.json)
        self.validate_json(json_response, self.lms_user.to_schema)

    @allure.id("3893")
    @allure.title('Get lms user (API)')
    def test_get_lms_user(self, lms_user):
        response = get_lms_user(lms_user['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_json(json_response, lms_user)
        self.validate_json(json_response, self.lms_user.to_schema)

    @allure.id("3888")
    @allure.title('Query lms users (API)')
    @pytest.mark.parametrize('query', to_sort_query(lms_user.to_json, exclude=lms_user.related_fields()))
    def test_query_lms_users(self, query):
        response = get_lms_users_query(query)

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("3890")
    @allure.title('Check authorization for lms users endpoints (API)')
    @pytest.mark.parametrize('endpoint', lms_users_methods, ids=to_method_param)
    def test_check_authorization_for_lms_users_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
