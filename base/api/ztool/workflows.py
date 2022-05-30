import allure
from api_manager import post, get, put

from base.api.base import Z_TOOL_API_URL


def get_workflow(request_id: str, workflow_id: str, user: dict = None):
    with allure.step(f'Getting workflow with id "{workflow_id}"'):
        return get(Z_TOOL_API_URL + f'/request/{request_id}/workflows/{workflow_id}', user=user)


def get_workflows(request_id: str, user: dict = None):
    with allure.step(f'Getting activities with request_id "{request_id}"'):
        return get(Z_TOOL_API_URL + f'/request/{request_id}/workflows', user=user)


def submit_workflow(request_id: str, workflow_id: str, user: dict = None):
    with allure.step(f'Submitting workflow with id "{workflow_id}"'):
        return put(Z_TOOL_API_URL + f'/request/{request_id}/workflows/{workflow_id}/submit', user=user)


def send_submitted_workflow_to_grading(request_id: str, user: dict = None):
    with allure.step(f'Sending submitted workflows to grading state'):
        return post(Z_TOOL_API_URL + f'/request/{request_id}/workflows/sendSubmittedToGrading', user=user)


def send_approved_workflow_to_finished(request_id: str, user: dict = None):
    with allure.step(f'Sending approved workflows to finished state'):
        return post(Z_TOOL_API_URL + f'/request/{request_id}/workflows/sendApprovedToFinished', user=user)


def grade_workflow(request_id: str, workflow_id: str, payload: dict, user: dict = None):
    with allure.step(f'Grading workflow with id "{workflow_id}"'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/workflows/{workflow_id}/grade'
        return put(endpoint, json=payload, user=user)


def approve_workflow(request_id: str, workflow_id: str, user: dict = None):
    with allure.step(f'Approving workflow with id "{workflow_id}"'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/workflows/{workflow_id}/approve'
        return put(endpoint, user=user)


def get_workflow_answers(request_id: str, workflow_id: str, user: dict = None):
    with allure.step(f'Getting answers for workflow with id "{workflow_id}"'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/workflows/{workflow_id}/answers'
        return get(endpoint, user=user)


def undo_submit_workflow(request_id: str, workflow_id: str, user: dict = None):
    with allure.step(f'Undo submission for workflow with id "{workflow_id}"'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/workflows/{workflow_id}/undo_submit'
        return put(endpoint, user=user)


def undo_grade_workflow(request_id: str, workflow_id: str, user: dict = None):
    with allure.step(f'Undo grading for workflow with id "{workflow_id}"'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/workflows/{workflow_id}/undo_grade'
        return put(endpoint, user=user)


def revoke_in_grading_workflow_to_progress(request_id: str, workflow_id: str, user: dict = None):
    with allure.step(f'Revoke in grading workflow with id "{workflow_id}" to progress'):
        endpoint = Z_TOOL_API_URL + f'/request/{request_id}/workflows/{workflow_id}/revoke-grading-to-progress'
        return put(endpoint, user=user)
