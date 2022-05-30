from http import HTTPStatus

import pytest
import requests
from assertions import validate_json, assert_truth, assert_all, assert_any, assert_attr, assert_json, \
    assert_response_status, assert_lte, assert_model_equal
from waiting import wait

from models.users.role import SupportedRoles
from models.users.user import Users
from models.utils.users.query import SortModel
from models.utils.users.validation import ValidationResultModel, CommandCompletionResultModel
from settings import USERS_API, Z_TOOL_API, IDENTITY_API, DEFAULT_USER
from utils.api.constants import APIState
from utils.assertions.files import assert_downloaded_file, assert_file_exists_in_bucket_folder, \
    assert_file_does_not_exists_in_bucket_folder

USERS_API_URL = USERS_API + '/api/v1'
Z_TOOL_API_URL = Z_TOOL_API + '/api/v1'
IDENTITY_API_URL = IDENTITY_API + '/api/v1'


def health_check():
    """
    :return:

    Checks if service is started or not.
    Also checks if default user exists in database
    Default timeout 120 seconds
    """
    wait(
        lambda: requests.get(USERS_API_URL + '/ready', verify=False).status_code == 200,
        timeout_seconds=120,
    )
    wait(
        lambda: Users.manager.is_exists(email=DEFAULT_USER['username']),
        timeout_seconds=120,
    )


class BaseAPI:
    """
    Super class for all other API tests classes.

    Contains base classes and methods.
    """
    validation_result_model = ValidationResultModel
    command_completion_result_model = CommandCompletionResultModel
    http = HTTPStatus
    state = APIState
    roles = SupportedRoles
    sort_model_users = SortModel.manager
    assert_all = staticmethod(assert_all)
    assert_any = staticmethod(assert_any)
    assert_lte = staticmethod(assert_lte)
    assert_attr = staticmethod(assert_attr)
    assert_json = staticmethod(assert_json)
    assert_truth = staticmethod(assert_truth)
    assert_model_equal = staticmethod(assert_model_equal)
    assert_response_status = staticmethod(assert_response_status)

    validate_json = staticmethod(validate_json)

    assert_downloaded_file = staticmethod(assert_downloaded_file)
    assert_file_exists_in_bucket_folder = staticmethod(assert_file_exists_in_bucket_folder)
    assert_file_does_not_exists_in_bucket_folder = staticmethod(assert_file_does_not_exists_in_bucket_folder)

    def get_validation_result(self, json_response: dict):
        """
        :param json_response: Any response body
        :return: Validation result from response body
        :raises: ``_pytest.outcomes.Failed``

        Used to get validation result from response body.
        If no validation result was found in the response body,
        then will raise an ``_pytest.outcomes.Failed`` exception.
        """
        completed = self.validation_result_model.completed.json
        errors = self.command_completion_result_model.errors.json
        try:
            return json_response[completed][errors]
        except KeyError:
            pytest.fail(f'Unable to get validation result from {json_response}')
