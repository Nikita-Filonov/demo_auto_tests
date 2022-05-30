import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_grading_scale_created(check_id, user=None):
    with allure.step(f'Checking if grading scale with id {check_id} was created'):
        return get(USERS_API_URL + f'/create-grading-scales/{check_id}', user=user)


def is_grading_scale_deleted(check_id, user=None):
    with allure.step(f'Checking if grading scale with id {check_id} was deleted'):
        return get(USERS_API_URL + f'/delete-grading-scales/{check_id}', user=user)


def is_grading_scale_updated(check_id, user=None):
    with allure.step(f'Checking if grading scale with id {check_id} was updated'):
        return get(USERS_API_URL + f'/update-grading-scales/{check_id}', user=user)
