import allure
from api_manager import get, post, lazy_request, Entities

from base.api.base import USERS_API_URL


def get_objective_workflows(user=None):
    with allure.step('Getting objectives workflows'):
        return get(USERS_API_URL + f'/objective-workflows', user=user)


def get_objective_workflow(objective_workflow_id, user=None):
    with allure.step(f'Getting objective workflow with id {objective_workflow_id}'):
        return get(USERS_API_URL + f'/objective-workflows/{objective_workflow_id}', user=user)


def get_started_objective_workflow(start_objective_workflow_id, user=None):
    with allure.step(f'Getting started objective workflow with id {start_objective_workflow_id}'):
        return get(USERS_API_URL + f'/start-objective-workflows/{start_objective_workflow_id}', user=user)


def get_started_objective_workflows(user=None):
    with allure.step('Getting started objective workflows'):
        return get(USERS_API_URL + f'/start-objective-workflows', user=user)


def get_objective_workflows_query(query, user=None):
    with allure.step(f'Getting objective workflows with query {query}'):
        return get(USERS_API_URL + '/objective-workflows/query', user=user, params=query)


@lazy_request(Entities.OBJECTIVE_WORKFLOW, 'Checking while objective workflow successfully submitted')
def submit_objective_workflow(payload, user=None):
    with allure.step(f'Submitting objective workflow with payload {payload}'):
        return post(USERS_API_URL + f'/submit-objective-workflows', json=payload, user=user)


def get_submitted_objective_workflow(submit_objective_workflow_id, user=None):
    with allure.step(f'Getting submitted objective workflow with id {submit_objective_workflow_id}'):
        return get(USERS_API_URL + f'/submit-objective-workflows/{submit_objective_workflow_id}', user=user)


def get_submitted_objective_workflows(user=None):
    with allure.step('Getting submitted objective workflows'):
        return get(USERS_API_URL + f'/submit-objective-workflows', user=user)
