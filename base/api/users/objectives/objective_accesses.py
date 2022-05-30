import allure
from api_manager import get, delete, lazy_request, Entities

from base.api.base import USERS_API_URL


@allure.step('Getting objective accesses')
def get_objective_accesses(user=None):
    return get(USERS_API_URL + f'/objective-accesses', user=user)


@lazy_request(Entities.OBJECTIVE_ACCESS)
def delete_objective_access(objective_accesses_id, user=None):
    with allure.step(f'Deleting objective access with id {objective_accesses_id}'):
        return delete(USERS_API_URL + f'/objective-accesses/{objective_accesses_id}', user=user)


def get_objective_access(objective_accesses_id, user=None):
    with allure.step(f'Getting objective access with id {objective_accesses_id}'):
        return get(USERS_API_URL + f'/objective-accesses/{objective_accesses_id}', user=user)


def get_objective_accesses_query(query, user=None):
    with allure.step(f'Getting objective accesses with query {query}'):
        return get(USERS_API_URL + f'/objective-accesses/query', user=user, params=query)
