import allure
from api_manager import get, post, put, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL
from models.users.user import Users
from utils.typing import EntityId


def get_user_roles(user=None):
    with allure.step('Getting user roles'):
        return get(USERS_API_URL + '/users/me/roles', user=user)


def get_user_permissions(user=None):
    with allure.step('Getting user permissions'):
        return get(USERS_API_URL + '/users/me/permissions', user=user)


def get_user(user_id: EntityId, user=None):
    with allure.step(f'Getting user with id {user_id}'):
        return get(USERS_API_URL + f'/users/{user_id}', user=user)


def get_users(user=None):
    with allure.step('Getting users'):
        return get(USERS_API_URL + '/users', user=user)


def get_users_query(query, user=None):
    with allure.step(f'Getting users with query {query}'):
        return get(USERS_API_URL + '/users/query', user=user, params=query)


def get_user_objective_workflow_aggregates(user_id: EntityId, user=None):
    with allure.step(f'Getting objective workflow aggregates for user with id "{user_id}"'):
        return get(USERS_API_URL + f'/users/{user_id}/objective-workflow-aggregates', user=user)


@lazy_request(Entities.USER)
def create_user(payload: dict, user=None):
    with allure.step(f'Creating user with data {prettify_json(payload)}'):
        return post(USERS_API_URL + '/users', user=user, json=payload)


@lazy_request(Entities.USER)
def update_user(user_id: EntityId, payload: dict, user=None):
    with allure.step(f'Updating user with id {user_id} to payload {prettify_json(payload)}'):
        return put(USERS_API_URL + f'/users/{user_id}', json=payload, user=user)


def create_user_with_password(account: dict) -> dict:
    """Used to create user with password"""
    user_payload = {
        **Users.manager.to_json,
        'email': account['email'],
        'username': account['email'],
        'id': account['id']
    }
    return create_user(user_payload).json()
