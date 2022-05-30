import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_role_patterns_created(role_pattern_id, user=None):
    with allure.step(f'Checking if role pattern with id {role_pattern_id} was created'):
        return get(USERS_API_URL + f'/create-role-patterns/{role_pattern_id}', user=user)


def is_role_patterns_updated(role_pattern_id, user=None):
    with allure.step(f'Checking if role pattern with id {role_pattern_id} was updated'):
        return get(USERS_API_URL + f'/update-role-patterns/{role_pattern_id}', user=user)


def is_role_patterns_deleted(role_pattern_id, user=None):
    with allure.step(f'Checking if role pattern with id {role_pattern_id} was deleted'):
        return get(USERS_API_URL + f'/delete-role-patterns/{role_pattern_id}', user=user)
