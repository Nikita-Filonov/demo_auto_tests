import allure
from api_manager import get, put, lazy_request, Entities, prettify_json

from base.api.base import USERS_API_URL


@allure.step('Getting objectives')
def get_objectives(user=None):
    return get(USERS_API_URL + f'/objectives', user=user)


def get_objectives_query(query, user=None):
    with allure.step(f'Getting objectives with query {query}'):
        return get(USERS_API_URL + '/objectives/query', user=user, params=query)


@lazy_request(Entities.OBJECTIVE)
def update_objective(objective_id, payload, user=None):
    with allure.step(f'Updating objective with id {objective_id} to payload {prettify_json(payload)}'):
        return put(USERS_API_URL + f'/objectives/{objective_id}', user=user, json=payload)


def get_objective(objective_id, user=None):
    with allure.step(f'Getting objective with id {objective_id}'):
        return get(USERS_API_URL + f'/objectives/{objective_id}', user=user)


def get_objective_resource_link(objective_id, role, workflow_id=None, user=None):
    with allure.step(f'Getting objective resource link with id {objective_id} and role "{role}"'):
        endpoint = f'/objectives/{objective_id}/resource-link?role={role}'
        if workflow_id:
            endpoint += f'&workflowId={workflow_id}'

        return get(USERS_API_URL + endpoint, user=user)


def get_objective_resource_form(objective_id, user=None):
    with allure.step(f'Getting objective with id {objective_id} resource from'):
        return get(USERS_API_URL + f'/objectives/{objective_id}/resource-form', user=user)


def get_objective_objective_records(objective_id, user=None):
    with allure.step(f'Getting objective with id {objective_id} objective records'):
        return get(USERS_API_URL + f'/objectives/{objective_id}/objective-records', user=user)


def get_objective_objective_accesses(objective_id, user=None):
    with allure.step(f'Getting objective access with id {objective_id}'):
        return get(USERS_API_URL + f'/objectives/{objective_id}/objective-accesses', user=user)
