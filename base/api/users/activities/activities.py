import allure
from api_manager import get, put, Entities, lazy_request, prettify_json

from base.api.base import USERS_API_URL


def get_activities(user=None):
    with allure.step('Getting activities'):
        return get(USERS_API_URL + f'/activities', user=user)


@lazy_request(Entities.ACTIVITY)
def update_activity(activity_id, payload, user=None):
    with allure.step(f'Updating activity with id {activity_id} to payload {prettify_json(payload)}'):
        return put(USERS_API_URL + f'/activities/{activity_id}', user=user, json=payload)


def get_activity(activity_id, user=None):
    with allure.step(f'Getting activity with id {activity_id}'):
        return get(USERS_API_URL + f'/activities/{activity_id}', user=user)


def get_activities_query(query, user=None):
    with allure.step(f'Getting activities with query {query}'):
        return get(USERS_API_URL + '/activities/query', user=user, params=query)
