import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_lms_user_created(check_id: str, user: dict = None):
    with allure.step(f'Checking if lms user with id {check_id} was created'):
        return get(USERS_API_URL + f'/create-lms-users/{check_id}', user=user)


def is_lms_user_updated(check_id: str, user: dict = None):
    with allure.step(f'Checking if lms user with id {check_id} was updated'):
        return get(USERS_API_URL + f'/update-lms-users/{check_id}', user=user)
