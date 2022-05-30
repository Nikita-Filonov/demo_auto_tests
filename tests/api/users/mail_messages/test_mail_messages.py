import uuid

import allure
import pytest

from base.api.base import BaseAPI
from base.api.users.mail_messages.mail_messages import get_mail_messages, get_mail_message, get_mail_messages_query
from models.users.mail_message import MailMessages
from parameters.api.users.mail_messages import mail_messages_methods
from settings import RERUNS, RERUNS_DELAY
from utils.api.users.common import Endpoint
from utils.api.users.permissions import check_authorization_for_endpoint
from utils.api.utils import to_sort_query
from utils.formatters.parametrization import to_method_param
from utils.utils import random_string, find


@pytest.mark.api
@pytest.mark.mail_messages
@allure.epic('Core LMS')
@allure.feature('Mail messages')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestMailMessagesApi(BaseAPI):
    mail_message = MailMessages.manager

    @allure.id("554")
    @allure.title('Get mail messages (API)')
    def test_get_mail_messages(self):
        response = get_mail_messages()
        self.assert_response_status(response.status_code, self.http.OK)

    @allure.id("553")
    @pytest.mark.parametrize('query', to_sort_query(mail_message.to_json, exclude=mail_message.related_fields()))
    @allure.title('Query mail messages (API)')
    def test_query_mail_messages(self, query):
        response = get_mail_messages_query(query)

        self.assert_response_status(response.status_code, self.http.OK)
        self.validate_json(response.json(), self.sort_model_users.to_schema)

    @allure.id("555")
    @allure.title('Create user and check mail messages (API)')
    def test_create_user_and_check_mail_messages(self, user_function):
        mail_messages = get_mail_messages()
        is_mail_message_exist = find(
            lambda mail_message: mail_message['toAddress'] == user_function['email'],
            mail_messages.json()
        )

        self.assert_response_status(mail_messages.status_code, self.http.OK)
        self.assert_truth(is_mail_message_exist, 'Mail message')

    @allure.id("552")
    @allure.title('Get mail message (API)')
    def test_get_mail_message(self, user_function, mail_message):
        response = get_mail_message(mail_message['mail_message_id'])
        json_response = response.json()

        self.assert_response_status(response.status_code, self.http.OK)
        self.assert_attr(json_response['id'], mail_message['mail_message_id'], 'Mail message id')
        self.assert_attr(json_response['toAddress'], user_function['email'], 'Email address')

    @allure.id("556")
    @allure.title('Get not existing mail message (API)')
    def test_get_not_existing_mail_message(self):
        response = get_mail_message(uuid.uuid4())
        self.assert_response_status(response.status_code, self.http.NOT_FOUND)

    @allure.id("558")
    @allure.title('Get mail message with wrong id (API)')
    def test_get_mail_message_with_wrong_id(self):
        response = get_mail_message(random_string())
        self.assert_response_status(response.status_code, self.http.BAD_REQUEST)

    @allure.id("910")
    @allure.title('Check authorization for mail messages endpoints (API)')
    @pytest.mark.parametrize('endpoint', mail_messages_methods, ids=to_method_param)
    def test_check_authorization_for_mail_messages_endpoints(self, endpoint):
        check_authorization_for_endpoint(Endpoint(**endpoint))
