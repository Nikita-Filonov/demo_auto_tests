import allure
from api_manager import get, post, delete, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL


@allure.step('Getting group users')
def get_group_users(user=None):
    return get(USERS_API_URL + f'/group-users', user=user)


def get_group_users_query(query, user=None):
    with allure.step(f'Getting group users with query {query}'):
        return get(USERS_API_URL + f'/group-users/query', user=user, params=query)


@lazy_request(Entities.GROUP_USER)
def create_group_user(payload, user=None):
    with allure.step(f'Creating group user with data {prettify_json(payload)}'):
        return post(USERS_API_URL + f'/group-users', user=user, json=payload)


@lazy_request(Entities.GROUP_USER)
def delete_group_user(group_user_id, user=None):
    with allure.step(f'Deleting group user with id {group_user_id}'):
        return delete(USERS_API_URL + f'/group-users/{group_user_id}', user=user)


def get_group_user(group_user_id, user=None):
    with allure.step(f'Getting group user with id {group_user_id}'):
        return get(USERS_API_URL + f'/group-users/{group_user_id}', user=user)
