import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_tenant_setting_created(tenant_setting_id, user=None):
    with allure.step(f'Checking if tenant setting with id {tenant_setting_id} was created'):
        return get(USERS_API_URL + f'/create-tenant-settings/{tenant_setting_id}', user=user)


def is_tenant_setting_deleted(tenant_setting_id, user=None):
    with allure.step(f'Checking if tenant setting with id {tenant_setting_id} was deleted'):
        return get(USERS_API_URL + f'/delete-tenant-settings/{tenant_setting_id}', user=user)


def is_tenant_setting_updated(tenant_setting_id, user=None):
    with allure.step(f'Checking if tenant setting with id {tenant_setting_id} was updated'):
        return get(USERS_API_URL + f'/update-tenant-settings/{tenant_setting_id}', user=user)
