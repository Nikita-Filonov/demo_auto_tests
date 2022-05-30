from typing import Dict

import allure
from api_manager import post, get, put, delete, patch, prettify_json
from typing.io import BinaryIO

from base.api.base import Z_TOOL_API_URL


def create_answer(request_id: str, payload: dict, user: dict = None):
    with allure.step(f'Creating answer with data {prettify_json(payload)}'):
        return post(Z_TOOL_API_URL + f'/request/{request_id}/answers', json=payload, user=user)


def update_answer(request_id: str, answer_id: str, payload: dict, user: dict = None):
    with allure.step(f'Updating answer with id "{answer_id}" to payload {prettify_json(payload)}'):
        return put(Z_TOOL_API_URL + f'/request/{request_id}/answers/{answer_id}', user=user, json=payload)


def delete_answer(request_id: str, answer_id: str, user: dict = None):
    with allure.step(f'Deleting answer with id "{answer_id}"'):
        return delete(Z_TOOL_API_URL + f'/request/{request_id}/answers/{answer_id}', user=user)


def get_answer(request_id: str, answer_id: str, user: dict = None):
    with allure.step(f'Getting answer with id "{answer_id}"'):
        return get(Z_TOOL_API_URL + f'/request/{request_id}/answers/{answer_id}', user=user)


def attach_file_to_answer(request_id: str, answer_id: str, files: Dict[str, BinaryIO], user: dict = None):
    with allure.step(f'Attaching file "{files}" to answer with id "{answer_id}"'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/answers/{answer_id}/attachments'
        return post(endpoint, files=files, user=user)


def delete_attachment_from_answer(request_id: str, answer_id: str, attachment_id: str, user: dict = None):
    with allure.step(f'Deleting attachment with id "{attachment_id}" from answer with id "{answer_id}"'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/answers/{answer_id}/attachments/{attachment_id}'
        return delete(endpoint, user=user)


def update_attachment_in_answer(request_id: str, answer_id: str, attachment_id: str, payload: dict, user: dict = None):
    with allure.step(f'Updating attachment with id "{attachment_id}" from answer '
                     f'with id "{answer_id}", to payload {prettify_json(payload)}'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/answers/{answer_id}/attachment/{attachment_id}'
        return patch(endpoint, user=user, json=payload)


def get_attachment_link_from_answer(request_id: str, answer_id: str, attachment_id: str, user: dict = None):
    with allure.step(f'Getting attachment link with id "{attachment_id}" from answer with id "{answer_id}"'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/answers/{answer_id}/attachments/{attachment_id}/download'
        return get(endpoint, user=user)


def upload_feedback_attachment_to_answer(request_id: str, answer_id: str, file_path: str, user: dict = None):
    with allure.step(f'Uploading feedback attachment to answer with id "{answer_id}"'):
        files = {'formFile': open(file_path, 'rb')}
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/answers/{answer_id}/feedback-attachments'
        return post(endpoint, files=files, user=user)


def delete_feedback_attachment_from_answer(request_id: str, answer_id: str, attachment_id: str, user: dict = None):
    with allure.step(f'Deleting feedback attachment with id "{attachment_id}" from answer with id "{answer_id}"'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/answers/{answer_id}/feedback-attachments/{attachment_id}'
        return delete(endpoint, user=user)


def update_feedback_attachment_in_answer(request_id: str, answer_id: str, attachment_id: str, payload: dict,
                                         user: dict = None):
    with allure.step(f'Updating feedback attachment with id "{attachment_id}" '
                     f'from answer with id "{answer_id}", to payload {prettify_json(payload)}'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/answers/{answer_id}/feedback-attachments/{attachment_id}'
        return patch(endpoint, user=user, json=payload)


def get_feedback_attachment_link_from_answer(request_id: str, answer_id: str, attachment_id: str, user: dict = None):
    with allure.step(f'Getting feedback attachment link with id "{attachment_id}" from answer with id "{answer_id}"'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/answers/{answer_id}/' \
                                    f'feedback-attachments/{attachment_id}/download'
        return get(endpoint, user=user)
