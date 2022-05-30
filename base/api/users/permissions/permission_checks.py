import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_permission_created(permission_id, user=None):
    with allure.step(f'Checking if permission with id {permission_id} was created'):
        return get(USERS_API_URL + f'/create-permissions/{permission_id}', user=user)


def is_permission_updated(permission_id, user=None):
    with allure.step(f'Checking if permission with id {permission_id} was updated'):
        return get(USERS_API_URL + f'/update-permissions/{permission_id}', user=user)
