import allure
from api_manager import get, prettify_json

from base.api.base import USERS_API_URL


def get_not_started_reports(query: dict, user: dict = None):
    with allure.step(f'Getting not started reports with query {prettify_json(query)}'):
        return get(USERS_API_URL + f'/not-started-reports/query', user=user, params=query)


def get_for_grading_reports(query: dict, user: dict = None):
    with allure.step(f'Getting for grading reports with query {prettify_json(query)}'):
        return get(USERS_API_URL + f'/for-grading-reports/query', user=user, params=query)


def get_payroll_reports(query: dict, user: dict = None):
    with allure.step(f'Getting payroll reports with query {prettify_json(query)}'):
        return get(USERS_API_URL + f'/payroll-reports/query', user=user, params=query)


def get_user_reports(query: dict, user: dict = None):
    with allure.step(f'Getting user reports with query {prettify_json(query)}'):
        return get(USERS_API_URL + f'/user-reports/query', user=user, params=query)


def get_objective_reports(query, user=None):
    with allure.step(f'Getting objectives reports with query {prettify_json(query)}'):
        return get(USERS_API_URL + f'/objective-reports/query', user=user, params=query)
