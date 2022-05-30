import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_role_pattern_permission_created(check_id, user=None):
    with allure.step(f'Checking if role pattern permission with id {check_id} was created'):
        return get(USERS_API_URL + f'/create-role-pattern-permissions/{check_id}', user=user)


def is_role_pattern_permission_deleted(check_id, user=None):
    with allure.step(f'Checking if role pattern permission with id {check_id} was deleted'):
        return get(USERS_API_URL + f'/delete-role-pattern-permissions/{check_id}', user=user)
