import allure
from api_manager import get, post, put, delete, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL


@allure.step('Getting role patterns')
def get_role_patterns(user=None):
    return get(USERS_API_URL + f'/role-patterns', user=user)


def get_role_patterns_query(query, user=None):
    with allure.step(f'Getting role patterns with query {query}'):
        return get(USERS_API_URL + '/role-patterns/query', user=user, params=query)


@lazy_request(Entities.ROLE_PATTERN)
def create_role_pattern(payload, user=None):
    with allure.step(f'Creating role pattern with data {prettify_json(payload)}'):
        return post(USERS_API_URL + f'/role-patterns', json=payload, user=user)


@lazy_request(Entities.ROLE_PATTERN)
def update_role_pattern(role_pattern_id, payload, user=None):
    with allure.step(f'Updating role pattern with id {role_pattern_id} to payload {prettify_json(payload)}'):
        return put(USERS_API_URL + f'/role-patterns/{role_pattern_id}', json=payload, user=user)


@lazy_request(Entities.ROLE_PATTERN)
def delete_role_pattern(role_pattern_id, user=None):
    with allure.step(f'Deleting role pattern with id {role_pattern_id}'):
        return delete(USERS_API_URL + f'/role-patterns/{role_pattern_id}', user=user)


def get_role_pattern(role_pattern_id, user=None):
    with allure.step(f'Getting role pattern with id {role_pattern_id}'):
        return get(USERS_API_URL + f'/role-patterns/{role_pattern_id}', user=user)
