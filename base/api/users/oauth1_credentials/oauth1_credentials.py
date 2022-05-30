import allure
from api_manager import get, put, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL


@allure.step('Getting oauth1 credentials')
def get_oauth1_credentials(user=None):
    return get(USERS_API_URL + f'/o-auth1-credentials', user=user)


@lazy_request(Entities.OAUTH1_CREDENTIALS)
def update_oauth1_credential(oauth1_credentials_id, payload, user=None):
    with allure.step(f'Updating oauth1 credential with id {oauth1_credentials_id} '
                     f'to payload {prettify_json(payload)}'):
        return put(USERS_API_URL + f'/o-auth1-credentials/{oauth1_credentials_id}', json=payload, user=user)


def get_oauth1_credential(oauth1_credentials_id, user=None):
    with allure.step(f'Getting oauth1 credentials with id {oauth1_credentials_id}'):
        return get(USERS_API_URL + f'/o-auth1-credentials/{oauth1_credentials_id}', user=user)


def get_oauth1_credentials_query(query, user=None):
    with allure.step(f'Getting oauth1 credentials with query {query}'):
        return get(USERS_API_URL + f'/o-auth1-credentials/query', user=user, params=query)
