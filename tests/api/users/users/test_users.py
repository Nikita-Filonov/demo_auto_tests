import json

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.users.users import create_user, get_user, update_user, get_users, get_users_query, \
    get_user_permissions, get_user_objective_workflow_aggregates, get_user_roles
from models.users.activity import Activities
from models.users.group import Groups
from models.users.permission import Permissions
from models.users.role import SupportedRoles, Roles
from models.users.user import Users
from parameters.api.users.users import user_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param


@pytest.mark.api
@pytest.mark.users
@allure.epic('Core LMS')
@allure.feature('Users')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestUsersApi(BaseAPI):
    user = Users.manager

    @allure.id("418")
    @allure.title('Create user (API)')
    def test_create_user(self):
        payload = self.user.to_json
        response = create_user(payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], payload['id'], Users.user_id.json)
        self.assert_attr(json_response['username'], payload['username'], Users.username.json)
        self.assert_attr(json_response['email'], payload['email'], Users.email.json)
        self.validate_json(json_response, self.user.to_schema)

    @allure.id("416")
    @allure.title('Get users (API)')
    def test_get_users(self):
        response = get_users()
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(json_response, self.user.to_array_schema)

    @allure.id("419")
    @allure.title('Update user (API)')
    def test_update_user(self, user_function):
        update_payload = self.user.to_json

        response = update_user(user_function['id'], update_payload)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], user_function['id'], Users.user_id.json)
        self.assert_attr(json_response['username'], update_payload['username'], Users.username.json)
        self.assert_attr(json_response['email'], update_payload['email'], Users.email.json)
        self.validate_json(json_response, self.user.to_schema)

    @allure.id("417")
    @allure.title('Get user (API)')
    def test_get_user(self, user_function):
        response = get_user(user_function['id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_json(json_response, user_function)
        self.validate_json(json_response, self.user.to_schema)

    @allure.id("4064")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-905',
        name='Remove "roles" from permissions json serialization'
    )
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-906',
        name='User permissions endpoint tenant always null'
    )
    @allure.title('Checking user permissions for different scopes (API)')
    @pytest.mark.parametrize(
        'user_with_permissions_function',
        [Activities.SCOPE, Users.SCOPE, [*Groups.SCOPE, *Users.SCOPE]],
        indirect=['user_with_permissions_function']
    )
    def test_checking_user_permissions_for_different_scopes(self, user_with_permissions_function: dict):
        scopes = user_with_permissions_function['scopes']
        response = get_user_permissions(json.dumps(user_with_permissions_function))
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(len(scopes), len(json_response), 'Number of permissions')
        self.validate_json(json_response, Permissions.manager.to_array_schema)
        self.assert_all(json_response, scopes, 'Permissions',
                        [Permissions.name.json, Permissions.scope.json, Permissions.scope_type.json])

    @allure.id("5376")
    @allure.title('Getting user roles (API)')
    @pytest.mark.parametrize(
        'user_with_roles_function',
        [
            [SupportedRoles.AUTHOR, SupportedRoles.LEARNER],
            [SupportedRoles.AUTHOR, SupportedRoles.ADMINISTRATOR],
            [SupportedRoles.AUTHOR, SupportedRoles.INSTRUCTOR],
            [SupportedRoles.AUTHOR, SupportedRoles.TENANT_ADMIN],
            [SupportedRoles.LEARNER],
        ],
        indirect=['user_with_roles_function']
    )
    def test_getting_user_roles(self, user_with_roles_function):
        user, roles = user_with_roles_function
        response = get_user_roles(user=user)
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(len(roles), len(json_response), 'Number of roles')
        self.validate_json(json_response, Roles.manager.to_array_schema)
        self.assert_all(json_response, roles, 'Roles', [Roles.name.json, Roles.role_id.json])

    @allure.id("4065")
    @allure.title('Get user objective workflow aggregates (API)')
    def test_get_user_objective_workflow_aggregates(self, user_function):
        response = get_user_objective_workflow_aggregates(user_function['id'])
        self.assert_response_status(response.status_code, self.http.OK)

    @allure.id("1886")
    @allure.title('Query users (API)')
    @pytest.mark.parametrize('query', to_sort_query(user.to_json, exclude=user.related_fields()))
    def test_query_users(self, query):
        response = get_users_query(query)

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("918")
    @allure.title('Check authorization for users endpoints (API)')
    @pytest.mark.parametrize('endpoint', user_methods, ids=to_method_param)
    def test_check_authorization_for_users_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
