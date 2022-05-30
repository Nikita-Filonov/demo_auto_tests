import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_activity_created(check_id, user=None):
    with allure.step(f'Checking if activity with id {check_id} was created'):
        return get(USERS_API_URL + f'/create-activities/{check_id}', user=user)


def is_activity_updated(check_id, user=None):
    with allure.step(f'Checking if activity with id {check_id} was updated'):
        return get(USERS_API_URL + f'/update-activities/{check_id}', user=user)
