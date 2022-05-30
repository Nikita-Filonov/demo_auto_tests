import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_role_created(check_id, user=None):
    with allure.step(f'Checking if role with id {check_id} was created'):
        return get(USERS_API_URL + f'/create-roles/{check_id}', user=user)


def is_role_updated(check_id, user=None):
    with allure.step(f'Checking if role with id {check_id} was updated'):
        return get(USERS_API_URL + f'/update-roles/{check_id}', user=user)
