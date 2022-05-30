import allure
from api_manager import get, post, put, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL


@allure.step('Getting tenants')
def get_tenants(user=None):
    return get(USERS_API_URL + '/tenants', user=user)


@lazy_request(Entities.TENANT)
def create_tenant(payload, user=None):
    with allure.step(f'Creating tenant with data {prettify_json(payload)}'):
        return post(USERS_API_URL + '/tenants', json=payload, user=user)


@lazy_request(Entities.TENANT)
def update_tenant(tenant_id, payload, user=None):
    with allure.step(f'Updating tenant with id {tenant_id} to payload {prettify_json(payload)}'):
        return put(USERS_API_URL + f'/tenants/{tenant_id}', json=payload, user=user)


def get_tenants_query(query, user=None):
    with allure.step(f'Getting tenants with query {query}'):
        return get(USERS_API_URL + f'/tenants/query', user=user, params=query)


def get_tenant(tenant_id, user=None):
    with allure.step(f'Getting tenant with id {tenant_id}'):
        return get(USERS_API_URL + f'/tenants/{tenant_id}', user=user)
