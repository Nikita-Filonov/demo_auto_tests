import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_group_user_created(check_id, user=None):
    with allure.step(f'Checking if activity with id {check_id} was created'):
        return get(USERS_API_URL + f'/create-group-users/{check_id}', user=user)


def is_group_user_deleted(check_id, user=None):
    with allure.step(f'Checking if group with id {check_id} was deleted'):
        return get(USERS_API_URL + f'/delete-group-users/{check_id}', user=user)
