import allure
from api_manager import get, post, put, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL


def get_permissions(user=None):
    with allure.step(f'Getting permissions'):
        return get(USERS_API_URL + '/permissions', user=user)


def get_permissions_query(query, user=None):
    with allure.step(f'Getting permissions with query {query}'):
        return get(USERS_API_URL + f'/permissions/query', user=user, params=query)


@lazy_request(Entities.PERMISSION)
def create_permission(payload, user=None):
    with allure.step(f'Creating permission with data {prettify_json(payload)}'):
        return post(USERS_API_URL + f'/permissions', user=user, json=payload)


@lazy_request(Entities.PERMISSION)
def update_permission(permission_id, payload, user=None):
    with allure.step(f'Updating permission with id {permission_id} to payload {prettify_json(payload)}'):
        return put(USERS_API_URL + f'/permissions/{permission_id}', user=user, json=payload)


def get_permission(permission_id, user=None):
    with allure.step(f'Getting permission with id {permission_id}'):
        return get(USERS_API_URL + f'/permissions/{permission_id}', user=user)
