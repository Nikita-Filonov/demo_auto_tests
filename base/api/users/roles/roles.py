import allure
from api_manager import get, post, put, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL


@allure.step('Getting roles')
def get_roles(user=None):
    return get(USERS_API_URL + '/roles', user=user)


@lazy_request(Entities.ROLE)
def create_role(payload, user=None):
    with allure.step(f'Creating role with data {prettify_json(payload)}'):
        return post(USERS_API_URL + '/roles', json=payload, user=user)


@lazy_request(Entities.ROLE)
def update_role(role_id, payload, user=None):
    with allure.step(f'Updating role with id {role_id} to payload {prettify_json(payload)}'):
        return put(USERS_API_URL + f'/roles/{role_id}', json=payload, user=user)


def get_roles_query(query, user=None):
    with allure.step(f'Getting roles with query {query}'):
        return get(USERS_API_URL + '/roles/query', user=user, params=query)


def get_role(role_id, user=None):
    with allure.step(f'Getting role with id {role_id}'):
        return get(USERS_API_URL + f'/roles/{role_id}', user=user)


def get_role_permissions(role_id, user=None):
    with allure.step(f'Getting permissions of role with id {role_id}'):
        return get(USERS_API_URL + f'/roles/{role_id}/permissions', user=user)


def get_role_permission(role_id, permission_id, user=None):
    with allure.step(f'Getting permissions of role with id {role_id}'):
        return get(USERS_API_URL + f'/roles/{role_id}/permissions/{permission_id}', user=user)
