import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_objective_created(check_id, user=None):
    with allure.step(f'Checking if objective with id {check_id} was created'):
        return get(USERS_API_URL + f'/create-objectives/{check_id}', user=user)


def is_objective_updated(check_id, user=None):
    with allure.step(f'Checking if objective with id {check_id} was updated'):
        return get(USERS_API_URL + f'/update-objectives/{check_id}', user=user)
