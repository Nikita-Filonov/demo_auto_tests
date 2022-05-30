import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_tenant_created(check_id, user=None):
    with allure.step(f'Checking if tenant with id {check_id} was created'):
        return get(USERS_API_URL + f'/create-tenants/{check_id}', user=user)


def is_tenant_updated(check_id, user=None):
    with allure.step(f'Checking if tenant with id {check_id} was updated'):
        return get(USERS_API_URL + f'/update-tenants/{check_id}', user=user)
