import json
from http import HTTPStatus

from assertions import assert_response_status
from requests import Response

from parameters.api.users.activities import activity_methods
from parameters.api.users.grading_scales import grading_scales_methods
from parameters.api.users.group_users import group_user_methods
from parameters.api.users.groups import groups_methods
from parameters.api.users.oauth1_credentials import oauth1_credential_methods
from parameters.api.users.objective_accesses import objective_access_methods
from parameters.api.users.objective_records import objective_record_methods
from parameters.api.users.objective_workflow_aggregates import objective_workflow_aggregate_methods
from parameters.api.users.objective_workflows import objective_workflow_methods
from parameters.api.users.objectives import objective_methods
from parameters.api.users.permissions import permissions_methods
from parameters.api.users.resource_library import resource_library_methods
from parameters.api.users.role_pattern import role_pattern_methods
from parameters.api.users.role_pattern_permissions import role_pattern_permission_methods
from parameters.api.users.roles import roles_methods
from parameters.api.users.tenant_settings import tenant_settings_methods
from parameters.api.users.tenants import tenant_methods
from parameters.api.users.user_roles import user_role_methods
from parameters.api.users.users import user_methods
from utils.api.constants import RESPONSE, FORBIDDEN_RESPONSE
from utils.api.users.common import Endpoint
from utils.formatters.parametrization import to_method_param
from utils.utils import modify_list_of_dicts, call, unwrap

EXCLUDE_PERMISSIONS_ENDPOINTS = [
    'tenant_settings.get_tenant_settings',
    'tenant_settings.get_tenant_setting',
    'tenant_settings.get_tenant_settings_query'
]

METHODS = [
    *modify_list_of_dicts(activity_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(groups_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(roles_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(permissions_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(user_role_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(objective_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(group_user_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(user_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(tenant_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(tenant_settings_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(role_pattern_permission_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(oauth1_credential_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(objective_access_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(objective_record_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(objective_workflow_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(role_pattern_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(objective_workflow_aggregate_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(resource_library_methods, RESPONSE, FORBIDDEN_RESPONSE),
    *modify_list_of_dicts(grading_scales_methods, RESPONSE, FORBIDDEN_RESPONSE)
]


def make_methods_payload_for_permissions(*exclude_keys) -> list:
    """
    :param exclude_keys: Keys which should be excluded from methods list
    :return:

    In permissions autotests we have to check all instances/endpoints for 403
    status code. In pytest parametrize this would look like

    @pytest.mark.parametrize('endpoint', [
        {'method': get_activity, 'args': (activity_id,), 'response': 200},
        ...
        *modify_list_of_dicts(activity_methods, RESPONSE, FORBIDDEN_RESPONSE),
        *modify_list_of_dicts(groups_methods, RESPONSE, FORBIDDEN_RESPONSE),
        *modify_list_of_dicts(roles_methods, RESPONSE, FORBIDDEN_RESPONSE),
    ])

    In general we want to avoid duplicating code like shown above.
    This method is solution to avoid duplicates and exclude unnecessary
    methods by "key" property. So for example if we testing "Activity"
    model for permissions, then we want to exclude "activity" key, and
    include all others. In pytest parametrize this looks like:

    @pytest.mark.parametrize('endpoint', [
        {'method': get_activity, 'args': (activity_id,), 'response': 200},
        ...
        *make_methods_payload_for_permissions('activity')
    ])

    Pay attention that "METHODS" is global variable. This made because
    every time we import/use METHODS, it is creating all related instances,
    getting some values from API and database. We do not want to run all this
    stuff on each test, so while this variable is global it will create all
    instances once. And this wont affect our performance and autotests speed

    Example:
    METHODS = [
        {'key': 'groups.create'},
        {'key': 'groups.delete'},
        {'key': 'groups.get'},
        {'key': 'users.get'},
        {'key': 'users.create'},
        {'key': 'users.delete'},
    ]
    make_methods_payload_for_permissions('groups') ->
    [{'key': 'users.get'}, {'key': 'users.create'}, {'key': 'users.delete'}]

    make_methods_payload_for_permissions('groups', 'users.get') -> [{'key': 'users.create'}, {'key': 'users.delete'}]
    """
    # checking if all exclude_keys a in lower case
    if not all(key.islower() for key in exclude_keys):
        # is some of exclude_keys not in lower case
        # then convert them to lower case
        exclude_keys = [key.lower() for key in exclude_keys]

    filtered_methods = filter(
        # checking if any method key startswith key that's in exclude_keys,
        # and excluding them
        lambda m: not any(m['key'].startswith(key) for key in exclude_keys),
        METHODS  # all methods
    )
    return list(filtered_methods)


def scopes_assertion_message(response: Response, response_expected):
    """Small wrapper for assertion message for permission scopes"""
    return f'Check "{response.request.method}" on endpoint "{response.request.url}" failed. ' \
           f'Expected code {response_expected}, actual response {response.status_code}'


def check_permissions_for_entity(endpoint: Endpoint, user_with_permissions: dict):
    """
    :param endpoint: ``Endpoint`` object with args, method, key, expected_response attributes
    :param user_with_permissions: User with certain scope of permissions
    :raises: ``AssertionError``

    Used to authorize with ``user_with_permissions`` credentials and check that
    this user has or has not permissions to certain endpoint
    """
    to_method_param(endpoint)

    func, args, expected_response = endpoint.method, endpoint.args, endpoint.response
    response = unwrap(func)(*call(args), user=json.dumps(user_with_permissions))

    assert_message = scopes_assertion_message(response, expected_response)
    assert_response_status(response.status_code, expected_response, message=assert_message)


def check_authorization_for_endpoint(endpoint: Endpoint):
    """
    :param endpoint: ``Endpoint`` object with args, method, key, expected_response attributes
    :raises: ``AssertionError``

    Common wrapper which is used to check authorization on certain endpoint.
    Basically this method will call the ``Endpoint.method`` with invalid
    user credentials. So we expect that server should return 401 status code.
    """
    to_method_param(endpoint)

    func, args = endpoint.method, endpoint.args
    response = func(*call(args), user={'password': 'random'})

    assert_response_status(response.status_code, HTTPStatus.UNAUTHORIZED)
