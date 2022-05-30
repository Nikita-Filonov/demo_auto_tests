import allure
from api_manager import get, post, delete, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL


@allure.step('Getting user roles')
def get_user_roles(user=None):
    return get(USERS_API_URL + f'/user-roles', user=user)


@lazy_request(Entities.USER_ROLE)
def create_user_role(payload, user=None):
    with allure.step(f'Creating user role with data {prettify_json(payload)}'):
        return post(USERS_API_URL + f'/user-roles', json=payload, user=user)


@lazy_request(Entities.USER_ROLE)
def delete_user_role(user_role_id, user=None):
    with allure.step(f'Deleting user role with id {user_role_id}'):
        return delete(USERS_API_URL + f'/user-roles/{user_role_id}', user=user)


def get_user_role(user_role_id, user=None):
    with allure.step(f'Getting user role with id {user_role_id}'):
        return get(USERS_API_URL + f'/user-roles/{user_role_id}', user=user)


def get_user_role_query(query, user=None):
    with allure.step(f'Getting user roles with query {query}'):
        return get(USERS_API_URL + f'/user-roles/query', user=user, params=query)
