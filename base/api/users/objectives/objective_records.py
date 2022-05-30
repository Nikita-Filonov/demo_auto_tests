import allure
from api_manager import get

from base.api.base import USERS_API_URL


@allure.step('Getting objective records')
def get_objective_records(user=None):
    return get(USERS_API_URL + f'/objective-records', user=user)


def get_objective_records_query(query, user=None):
    with allure.step(f'Getting objectives records with query {query}'):
        return get(USERS_API_URL + f'/objective-records/query', user=user, params=query)


def get_objective_record(objective_records_id, user=None):
    with allure.step(f'Getting objective records with id {objective_records_id}'):
        return get(USERS_API_URL + f'/objective-records/{objective_records_id}', user=user)
