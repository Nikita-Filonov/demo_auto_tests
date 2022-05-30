import allure
from api_manager import get, post, delete, prettify_json

from base.api.base import USERS_API_URL


def upload_to_storage(payload, files, user=None):
    with allure.step(f'Uploading file {files} to storage with path {prettify_json(payload)}'):
        return post(USERS_API_URL + f'/storage', files=files, data=payload, user=user)


def get_from_storage(file_uri, user=None):
    with allure.step(f'Getting file {file_uri} from storage'):
        return get(USERS_API_URL + f'/storage/{file_uri}', user=user)


def delete_from_storage(file, user=None):
    with allure.step(f'Deleting file {file} from storage'):
        return delete(USERS_API_URL + f'/storage', json=file, user=user)
