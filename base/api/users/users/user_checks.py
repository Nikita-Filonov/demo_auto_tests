import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_user_created(check_id, user=None):
    with allure.step(f'Checking if user with id {check_id} was created'):
        return get(USERS_API_URL + f'/create-users/{check_id}', user=user)


def is_user_updated(check_id, user=None):
    with allure.step(f'Checking if user with id {check_id} was updated'):
        return get(USERS_API_URL + f'/update-users/{check_id}', user=user)
