import allure
from api_manager import post

from base.api.base import IDENTITY_API_URL


def create_account(payload):
    with allure.step(f'Creating account with data {payload}'):
        return post(IDENTITY_API_URL + f'/users', json=payload, with_auth=False)
