import allure
from api_manager import get, post, put, delete, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL


def get_tenant_settings(user=None):
    with allure.step(f'Getting tenant settings'):
        return get(USERS_API_URL + f'/tenant-settings', user=user)


def get_tenant_settings_query(query, user=None):
    with allure.step(f'Getting tenant settings with query {query}'):
        return get(USERS_API_URL + f'/tenant-settings/query', user=user, params=query)


@lazy_request(Entities.TENANT_SETTING)
def create_tenant_setting(payload, user=None):
    with allure.step(f'Creating tenant setting with data {prettify_json(payload)}'):
        return post(USERS_API_URL + f'/tenant-settings', user=user, json=payload)


@lazy_request(Entities.TENANT_SETTING)
def update_tenant_setting(tenant_setting_id, payload, user=None):
    with allure.step(f'Updating tenant setting with id {tenant_setting_id} to payload {prettify_json(payload)}'):
        return put(USERS_API_URL + f'/tenant-settings/{tenant_setting_id}', user=user, json=payload)


@lazy_request(Entities.TENANT_SETTING)
def delete_tenant_setting(tenant_setting_id, user=None):
    with allure.step(f'Deleting tenant setting with id {tenant_setting_id}'):
        return delete(USERS_API_URL + f'/tenant-settings/{tenant_setting_id}', user=user)


def get_tenant_setting(tenant_setting_id, user=None):
    with allure.step(f'Getting tenant setting with id {tenant_setting_id}'):
        return get(USERS_API_URL + f'/tenant-settings/{tenant_setting_id}', user=user)
