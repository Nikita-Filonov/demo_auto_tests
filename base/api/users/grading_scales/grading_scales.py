import allure
from api_manager import get, post, put, delete, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL


def get_grading_scales(user=None):
    with allure.step('Getting grading scales'):
        return get(USERS_API_URL + f'/grading-scales', user=user)


@lazy_request(Entities.GRADING_SCALE)
def create_grading_scale(payload, user=None):
    with allure.step(f'Creating grading scale with data {prettify_json(payload)}'):
        return post(USERS_API_URL + f'/grading-scales', user=user, json=payload)


@lazy_request(Entities.GRADING_SCALE)
def update_grading_scale(grading_scale_id, payload, user=None):
    with allure.step(f'Updating grading scale with id "{grading_scale_id}" to payload {prettify_json(payload)}'):
        return put(USERS_API_URL + f'/grading-scales/{grading_scale_id}', user=user, json=payload)


@lazy_request(Entities.GRADING_SCALE)
def delete_grading_scale(grading_scale_id, user=None):
    with allure.step(f'Deleting grading scale with id "{grading_scale_id}"'):
        return delete(USERS_API_URL + f'/grading-scales/{grading_scale_id}', user=user)


def get_grading_scale(grading_scale_id, user=None):
    with allure.step(f'Getting grading scale with id "{grading_scale_id}"'):
        return get(USERS_API_URL + f'/grading-scales/{grading_scale_id}', user=user)


def get_grading_scales_query(query, user=None):
    with allure.step(f'Getting grading scales with query {query}'):
        return get(USERS_API_URL + '/grading-scales/query', user=user, params=query)
