import allure
from api_manager import get, post, put, delete, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL
from utils.api.utils import encode_to_url
from utils.typing import PathLike


def get_resource_libraries(user=None):
    with allure.step(f'Getting resource libraries'):
        return get(USERS_API_URL + f'/resource-libraries', user=user)


def get_resource_libraries_query(query, user=None):
    with allure.step(f'Getting resource libraries with query {query}'):
        return get(USERS_API_URL + f'/resource-libraries/query', user=user, params=query)


@lazy_request(Entities.RESOURCE_LIBRARIES)
def create_resource_library(payload, user=None):
    with allure.step(f'Creating resource library with data {prettify_json(payload)}'):
        return post(USERS_API_URL + f'/resource-libraries', user=user, json=payload)


@lazy_request(Entities.RESOURCE_LIBRARIES)
def update_resource_library(resource_library_id, payload, user=None):
    with allure.step(f'Updating resource library with id {resource_library_id} to payload {prettify_json(payload)}'):
        return put(USERS_API_URL + f'/resource-libraries/{resource_library_id}', user=user, json=payload)


@lazy_request(Entities.RESOURCE_LIBRARIES)
def delete_resource_library(resource_library_id, user=None):
    with allure.step(f'Deleting resource library with id {resource_library_id}'):
        return delete(USERS_API_URL + f'/resource-libraries/{resource_library_id}', user=user)


def get_resource_library(resource_library_id, user=None):
    with allure.step(f'Getting resource library with id {resource_library_id}'):
        return get(USERS_API_URL + f'/resource-libraries/{resource_library_id}', user=user)


def get_resource_library_actions(resource_library_id, user=None):
    with allure.step(f'Getting resource library actions for library with id "{resource_library_id}"'):
        return get(USERS_API_URL + f'/resource-libraries/{resource_library_id}/actions', user=user)


def get_resource_library_resources(resource_library_id, user=None):
    with allure.step(f'Getting resource library resources for library with id "{resource_library_id}"'):
        return get(USERS_API_URL + f'/resource-libraries/{resource_library_id}/resources', user=user)


def get_resource_library_resources_in_path(resource_library_id: str, storage_path: PathLike, user=None):
    with allure.step(f'Getting resource library resources in a path "{storage_path}" '
                     f'for library with id "{resource_library_id}"'):
        url = USERS_API_URL + f'/resource-libraries/{resource_library_id}/resources/{encode_to_url(storage_path)}'
        return get(url, user=user)
