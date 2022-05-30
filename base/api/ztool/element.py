import allure
from api_manager import post, get, put, delete, prettify_json

from base.api.base import Z_TOOL_API_URL
from utils.utils import file_name_or_path_resolve


def create_element(request_id: str, payload: dict, user: dict = None):
    with allure.step(f'Creating element with data {prettify_json(payload)}'):
        return post(Z_TOOL_API_URL + f'/request/{request_id}/elements', user=user, json=payload)


def get_element(request_id: str, element_id: str, user: dict = None):
    with allure.step(f'Getting element with id "{element_id}"'):
        return get(Z_TOOL_API_URL + f'/request/{request_id}/elements/{element_id}', user=user)


def update_element(request_id: str, element_id: str, payload: dict, user: dict = None):
    with allure.step(f'Updating element with id "{element_id}" to payload {prettify_json(payload)}'):
        return put(Z_TOOL_API_URL + f'/request/{request_id}/elements/{element_id}', user=user, json=payload)


def delete_element(request_id: str, element_id: str, user: dict = None):
    with allure.step(f'Deleting element with id "{element_id}"'):
        return delete(Z_TOOL_API_URL + f'/request/{request_id}/elements/{element_id}', user=user)


def get_grades_of_element(request_id: str, element_id: str, user: dict = None):
    with allure.step(f'Getting grades for element with id "{element_id}"'):
        return get(Z_TOOL_API_URL + f'/request/{request_id}/elements/{element_id}/grades', user=user)


def update_grade_in_element(request_id: str, element_id: str, grade_id: str, payload: dict, user: dict = None):
    with allure.step(f'Updating grade with id "{grade_id}" to payload {prettify_json(payload)}'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/elements/{element_id}/grades/{grade_id}'
        return put(endpoint, json=payload, user=user)


def get_exercises_of_element(request_id: str, element_id: str, user: dict = None):
    with allure.step(f'Getting exercises for element with id "{element_id}"'):
        return get(Z_TOOL_API_URL + f'/request/{request_id}/elements/{element_id}/exercises', user=user)


def upload_textbook_attachment_to_element(request_id: str, element_id: str, payload: dict, user: dict = None):
    with allure.step(f'Uploading textbook attachment "{payload}" to element with id "{element_id}"'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/elements/{element_id}/textbook-attachments'
        return post(endpoint, json=payload, user=user)


def update_textbook_attachment_in_element(request_id: str,
                                          element_id: str,
                                          attachment_id: str,
                                          payload: dict,
                                          user: dict = None):
    with allure.step(f'Updating attachment with id "{attachment_id}" from element '
                     f'with id "{element_id}", to payload {prettify_json(payload)}'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/elements/{element_id}/textbook-attachments/{attachment_id}'
        return put(endpoint, json=payload, user=user)


def delete_textbook_attachment_from_element(request_id: str, element_id: str, attachment_id: str, user: dict = None):
    with allure.step(f'Deleting attachment with id "{attachment_id}" from element with id "{element_id}"'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/elements/{element_id}/textbook-attachments/{attachment_id}'
        return delete(endpoint, user=user)


def upload_file_to_element(request_id: str, element_id: str, file_path: str, user: dict = None):
    safe_file_name = file_name_or_path_resolve(file_path)
    files = {'file': open(file_path, 'rb')}
    with allure.step(f'Uploading file "{safe_file_name}" to element with id "{element_id}"'):
        return post(Z_TOOL_API_URL + f'/request/{request_id}/elements/{element_id}/files', files=files, user=user)


def get_element_files(request_id: str, element_id: str, user: dict = None):
    with allure.step(f'Getting files of element with id "{element_id}"'):
        return get(Z_TOOL_API_URL + f'/request/{request_id}/elements/{element_id}/files', user=user)


def delete_file_from_element(request_id: str, element_id: str, file_name: str, user: dict = None):
    with allure.step(f'Deleting file "{file_name}" from element with id "{element_id}"'):
        return delete(Z_TOOL_API_URL + f'/request/{request_id}/elements/{element_id}/files/{file_name}', user=user)


def update_file_in_element(request_id: str, element_id: str, file_name: str, payload: dict, user: dict = None):
    with allure.step(f'Updating file "{file_name}" in element with id '
                     f'"{element_id}" to payload {prettify_json(payload)}'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/elements/{element_id}/files/{file_name}'
        return put(endpoint, user=user, json=payload)
