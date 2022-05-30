import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_user_role_created(check_id, user=None):
    with allure.step(f'Checking if user role with id {check_id} was created'):
        return get(USERS_API_URL + f'/create-user-roles/{check_id}', user=user)


def is_user_role_deleted(check_id, user=None):
    with allure.step(f'Checking if user role with id {check_id} was deleted'):
        return get(USERS_API_URL + f'/delete-user-roles/{check_id}', user=user)
