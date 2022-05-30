import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.user_roles.user_roles import get_user_role_query, create_user_role, delete_user_role, \
    get_user_roles
from models.users.user_role import UserRoles
from parameters.api.users.user_roles import user_role_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.user_roles
@allure.epic('Core LMS')
@allure.feature('User Roles')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestUserRolesApi(BaseAPI):
    user_role = UserRoles.manager

    @allure.id("443")
    @allure.title('Create user role (API)')
    def test_create_user_role(self):
        payload = self.user_role.to_json
        response = create_user_role(payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], payload['id'], UserRoles.user_role_id.json)
        self.assert_attr(json_response['userId'], payload['userId'], UserRoles.user_id.json)
        self.assert_attr(json_response['role']['id'], payload['roleId'], UserRoles.role_id.json)
        self.validate_json(json_response, self.user_role.to_schema)

    @allure.title('Create user role negative (API)')
    def test_create_user_role_negative(self):
        payload = self.user_role.to_negative_json()

        response = create_user_role(payload)
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("442")
    @allure.title('Get user roles (API)')
    def test_get_user_roles(self):
        response = get_user_roles()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.user_role.to_array_schema)

    @allure.id("570")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-292',
        name='Can not delete User role'
    )
    @allure.title('Delete user role (API)')
    def test_delete_user_role(self, user_role):
        response = delete_user_role(user_role['id'])
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("438")
    @allure.title('Query user roles (API)')
    @pytest.mark.parametrize('query', to_sort_query(user_role.to_json, exclude=user_role.related_fields()))
    def test_query_user_roles(self, query):
        response = get_user_role_query(query)

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("902")
    @allure.title('Check authorization for user roles endpoints (API)')
    @pytest.mark.parametrize('endpoint', user_role_methods, ids=to_method_param)
    def test_check_authorization_for_user_roles_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
