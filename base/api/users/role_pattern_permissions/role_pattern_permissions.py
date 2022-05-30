import allure
from api_manager import get, post, delete, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL


@allure.step('Getting role pattern permissions')
def get_role_pattern_permissions(user=None):
    return get(USERS_API_URL + '/role-pattern-permissions', user=user)


def get_role_pattern_permissions_query(query, user=None):
    with allure.step(f'Getting role pattern permissions query {query}'):
        return get(USERS_API_URL + '/role-pattern-permissions/query', user=user, params=query)


@lazy_request(Entities.ROLE_PATTERN_PERMISSION)
def create_role_pattern_permission(payload, user=None):
    with allure.step(f'Creating role pattern permission with data {prettify_json(payload)}'):
        return post(USERS_API_URL + f'/role-pattern-permissions', json=payload, user=user)


@lazy_request(Entities.ROLE_PATTERN_PERMISSION)
def delete_role_pattern_permission(role_pattern_permission_id, user=None):
    with allure.step(f'Deleting role pattern permission with id {role_pattern_permission_id}'):
        return delete(USERS_API_URL + f'/role-pattern-permissions/{role_pattern_permission_id}', user=user)


def get_role_pattern_permission(role_pattern_permission_id, user=None):
    with allure.step(f'Getting role pattern permissions with id {role_pattern_permission_id}'):
        return get(USERS_API_URL + f'/role-pattern-permissions/{role_pattern_permission_id}', user=user)
