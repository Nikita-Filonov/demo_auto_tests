import allure
from api_manager import get, post, put, delete, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL


def get_groups(user=None):
    with allure.step(f'Getting groups'):
        return get(USERS_API_URL + f'/groups', user=user)


def get_groups_query(query, user=None):
    with allure.step(f'Getting groups with query {query}'):
        return get(USERS_API_URL + '/groups/query', user=user, params=query)


@lazy_request(Entities.GROUP)
def create_group(payload, user=None):
    with allure.step(f'Creating group with data {prettify_json(payload)}'):
        return post(USERS_API_URL + f'/groups', user=user, json=payload)


@lazy_request(Entities.GROUP)
def update_group(group_id, payload, user=None):
    with allure.step(f'Updating group with id {group_id} to payload {prettify_json(payload)}'):
        return put(USERS_API_URL + f'/groups/{group_id}', user=user, json=payload)


@lazy_request(Entities.GROUP)
def delete_group(group_id, user=None):
    with allure.step(f'Deleting group with id {group_id}'):
        return delete(USERS_API_URL + f'/groups/{group_id}', user=user)


def get_group(group_id, user=None):
    with allure.step(f'Getting group with id {group_id}'):
        return get(USERS_API_URL + f'/groups/{group_id}', user=user)
