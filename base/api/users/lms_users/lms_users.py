from typing import Union

import allure
from api_manager import get, post, put, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL


def get_lms_users(user: dict = None):
    with allure.step(f'Getting lms users'):
        return get(USERS_API_URL + f'/lms-users', user=user)


def get_lms_users_query(query: Union[str, dict], user: dict = None):
    with allure.step(f'Getting lms users with query {query}'):
        return get(USERS_API_URL + '/lms-users/query', user=user, params=query)


@lazy_request(Entities.LMS_USER)
def create_lms_user(payload: dict, user: dict = None):
    with allure.step(f'Creating lms user with data {prettify_json(payload)}'):
        return post(USERS_API_URL + f'/lms-users', user=user, json=payload)


@lazy_request(Entities.LMS_USER)
def update_lms_user(lms_user_id: str, payload: dict, user: dict = None):
    with allure.step(f'Updating lms user with id {lms_user_id} to payload {prettify_json(payload)}'):
        return put(USERS_API_URL + f'/lms-users/{lms_user_id}', user=user, json=payload)


def get_lms_user(lms_user_id: str, user: dict = None):
    with allure.step(f'Getting lms user with id {lms_user_id}'):
        return get(USERS_API_URL + f'/lms-users/{lms_user_id}', user=user)
