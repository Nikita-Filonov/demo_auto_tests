import allure
from api_manager import post, get, put, delete, prettify_json

from base.api.base import Z_TOOL_API_URL


def create_exercise(request_id: str, payload: dict, user: dict = None):
    with allure.step(f'Creating exercise with data {prettify_json(payload)}'):
        return post(Z_TOOL_API_URL + f'/request/{request_id}/exercises', json=payload, user=user)


def update_exercise(request_id: str, exercise_id: str, payload: dict, user: dict = None):
    with allure.step(f'Updating exercise with id "{exercise_id}" to payload {prettify_json(payload)}'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/exercises/{exercise_id}'
        return put(endpoint, json=payload, user=user)


def delete_exercise(request_id: str, exercise_id: str, user: dict = None):
    with allure.step(f'Deleting exercise with id "{exercise_id}"'):
        return delete(Z_TOOL_API_URL + f'/request/{request_id}/exercises/{exercise_id}', user=user)


def get_exercise(request_id: str, exercise_id: str, user: dict = None):
    with allure.step(f'Getting answer with id "{exercise_id}"'):
        return get(Z_TOOL_API_URL + f'/request/{request_id}/exercises/{exercise_id}', user=user)
