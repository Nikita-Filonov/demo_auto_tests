import allure
from api_manager import get

from base.api.base import USERS_API_URL


def get_objective_workflow_aggregates(user=None):
    with allure.step('Getting objective workflow aggregates'):
        return get(USERS_API_URL + f'/objective-workflow-aggregates', user=user)


def get_objective_workflow_aggregates_query(query, user=None):
    with allure.step(f'Getting objective workflow aggregates with query {query}'):
        return get(USERS_API_URL + '/objective-workflow-aggregates/query', user=user, params=query)
