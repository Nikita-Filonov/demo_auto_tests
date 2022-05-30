import allure
from api_manager import get

from base.api.base import USERS_API_URL


@allure.step('Getting mail messages')
def get_mail_messages(user=None):
    return get(USERS_API_URL + f'/mail-messages', user=user)


def get_mail_messages_query(query, user=None):
    with allure.step(f'Getting mail messages with query {query}'):
        return get(USERS_API_URL + f'/mail-messages/query', user=user, params=query)


def get_mail_message(mail_message_id, user=None):
    with allure.step(f'Getting mail message with id {mail_message_id}'):
        return get(USERS_API_URL + f'/mail-messages/{mail_message_id}', user=user)
