import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_resource_library_created(check_id, user=None):
    with allure.step(f'Checking if resource library with id {check_id} was created'):
        return get(USERS_API_URL + f'/create-resource-libraries/{check_id}', user=user)


def is_resource_library_deleted(check_id, user=None):
    with allure.step(f'Checking if resource library with id {check_id} was deleted'):
        return get(USERS_API_URL + f'/delete-resource-libraries/{check_id}', user=user)


def is_resource_library_updated(check_id, user=None):
    with allure.step(f'Checking if resource library with id {check_id} was updated'):
        return get(USERS_API_URL + f'/update-resource-libraries/{check_id}', user=user)
