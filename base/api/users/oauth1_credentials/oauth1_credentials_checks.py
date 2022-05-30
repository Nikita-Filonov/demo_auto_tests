import allure
from api_manager import get

from base.api.base import USERS_API_URL


def is_oauth1_credential_created(check_id, user=None):
    with allure.step(f'Checking if oauth1 credential with id {check_id} was created'):
        return get(USERS_API_URL + f'/create-o-auth1-credentials/{check_id}', user=user)


def is_oauth1_credential_updated(check_id, user=None):
    with allure.step(f'Checking if oauth1 credential with id {check_id} was updated'):
        return get(USERS_API_URL + f'/update-o-auth1-credentials/{check_id}', user=user)
