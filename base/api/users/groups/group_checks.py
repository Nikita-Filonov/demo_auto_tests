import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_group_created(check_id, user=None):
    with allure.step(f'Checking if group with id {check_id} was created'):
        return get(USERS_API_URL + f'/create-groups/{check_id}', user=user)


def is_group_deleted(check_id, user=None):
    with allure.step(f'Checking if group with id {check_id} was deleted'):
        return get(USERS_API_URL + f'/delete-groups/{check_id}', user=user)


def is_group_updated(check_id, user=None):
    with allure.step(f'Checking if group with id {check_id} was updated'):
        return get(USERS_API_URL + f'/update-groups/{check_id}', user=user)
