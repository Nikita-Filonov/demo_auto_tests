import allure
from api_manager import get, post, delete, prettify_json

from base.api.base import USERS_API_URL


@allure.step('Getting datagrid settings')
def get_data_grid_settings(user=None):
    return get(USERS_API_URL + f'/datagrid-settings', user=user)


def create_data_grid_setting(payload, user=None):
    with allure.step(f'Creating datagrid setting with data {prettify_json(payload)}'):
        return post(USERS_API_URL + f'/datagrid-settings', user=user, json=payload)


def delete_data_grid_setting(key, user=None):
    with allure.step(f'Deleting datagrid setting with key {key}'):
        return delete(USERS_API_URL + f'/datagrid-settings/{key}', user=user)


def get_data_grid_setting(key, user=None):
    with allure.step(f'Getting datagrid setting with key {key}'):
        return get(USERS_API_URL + f'/datagrid-settings/{key}', user=user)
