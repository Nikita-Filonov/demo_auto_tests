import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_objective_access_created(check_id, user=None):
    with allure.step(f'Checking if objective access with id {check_id} was created'):
        return get(USERS_API_URL + f'/create-objective-accesses/{check_id}', user=user)


def is_objective_access_deleted(check_id, user=None):
    with allure.step(f'Checking if objective access with id {check_id} was deleted'):
        return get(USERS_API_URL + f'/delete-objective-accesses/{check_id}', user=user)
