import json
from http import HTTPStatus
from typing import List, Callable, Optional, Union, Generator, Any

import allure
from requests import Response

from utils.api.response_validator.actions import ResponseActions
from utils.api.response_validator.exception import ValidatorError
from utils.api.response_validator.settings import VALIDATOR_ACTIONS
from utils.api.response_validator.utils import safe_codes, join_errors


class ResponseValidator:
    VALIDATOR = 'validator'

    def __init__(
            self,
            response: Response,
            func: Callable = None,
            error_codes: Optional[List[Union[int, HTTPStatus]]] = None,
            success_codes: Optional[List[Union[int, HTTPStatus]]] = None,
            response_model=None,
            actions: List[ResponseActions] = None,
            ignore_action_if: Callable = None,
            lazy_errors: bool = True,
    ):
        self.response = response
        self._func = func
        self._error_codes = error_codes
        self._success_codes = success_codes
        self._actions = actions or VALIDATOR_ACTIONS
        self._response_model = response_model
        self._lazy_errors = lazy_errors
        self._ignore_action_if = ignore_action_if

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.raise_for_validation()

    @property
    def func_name(self):
        """
        :return: Name of the function which we are decorating
        """
        return self._func.__name__

    def run_validation(self) -> Generator[str, Any, Any]:
        """
        :return: Returns generator object with errors which happened
        while running validators
        """
        for action in self._actions:
            validator = getattr(self, f'_{action.value}_{self.VALIDATOR}', None)

            if validator is None:
                raise ValidatorError(f'Validator "{action.value}" is not supported')

            if self._ignore_action_if and callable(self._ignore_action_if):
                if self._ignore_action_if(self.response, action.value):
                    continue

            yield validator()

        if self._response_model:
            yield self._response_model_validator()

    def raise_for_validation(self):
        """
        :raises: ``AssertionError``

        Used to extract errors from generator and if there is
        some errors, then it will raise ``AssertionError``
        """
        errors = list(filter(None, self.run_validation()))

        if errors:
            raise AssertionError('\n\n'.join(errors))

    def lazy_error(self, message: str):
        """
        :param message: Any error message
        :return: Message or raises assertion error
        :raises: ``AssertionError``

        Used to ensure if error should be lazy or not.
        If error is lazy, then method will return just string message,
        if error is not lazy then ``AssertionError`` will be
        raised immediately
        """
        if self._lazy_errors:
            return message

        raise AssertionError(message)

    def _status_code_validator(self) -> str:
        """
        Used to validate status code based on
        given settings ``error_codes``, ``success_codes``.

        Make sure you provided ``_success_codes`` OR ``_error_codes``.
        You can not use ``_success_codes`` and ``_error_codes`` at the same time.

        :return: Status code error message
        :raises: ``AssertionError``, ``ValidatorError``
        """
        with allure.step(f'Running status code validation for "{self.func_name}"'):
            status_code = self.response.status_code

            if (self._success_codes is not None) and (self._error_codes is not None):
                raise ValidatorError('Can not use "success_codes"/"error_codes" at same time')

            if self._error_codes is not None:
                error_codes = safe_codes(self._error_codes)

                with allure.step(f'Ensure that status code not in "{error_codes}" one of error codes'):
                    if status_code in error_codes:
                        joined_errors = join_errors(error_codes)
                        return self.lazy_error(
                            f'Response status code should not equal to one of {joined_errors}, '
                            f'but actually it equal to "{status_code}". '
                            f'Returned by "{self.func_name}"'
                        )

            if self._success_codes is not None:
                success_codes = safe_codes(self._success_codes)

                with allure.step(f'Checking that status code one of success codes "{success_codes}"'):
                    if status_code not in success_codes:
                        joined_successes = join_errors(success_codes)
                        return self.lazy_error(
                            f'Response status code should equal to one of {joined_successes}, '
                            f'but actually it equal to "{status_code}". '
                            f'Returned by "{self.func_name}"'
                        )

    def _json_validator(self):
        """
        Used to validate ability to get json from the response

        :return: Json error message
        :raises: ``AssertionError``
        """
        with allure.step(f'Ensure that we can get json from "{self.func_name}" response'):
            try:
                self.response.json()
            except json.decoder.JSONDecodeError:
                return self.lazy_error(
                    f'Unable to extract json from response returned by "{self.func_name}".\n'
                    f'Original response was: \n{self.response.content[:200]}'
                )

    def _ok_validator(self):
        """
        Common check, which can be used to ensure
        that response status code is less than 400.

        :return: Is response status code ok error message
        """
        with allure.step('Ensure that response status code is less than 400'):
            if not self.response.ok:
                return self.lazy_error(
                    f'Response status code is not less than 400. '
                    f'Actual response status code was "{self.response.status_code}". '
                    f'Returned by "{self.func_name}"'
                )

    def _response_model_validator(self):
        raise NotImplementedError('Model validation not implemented yet.')


def response_validator(
        success_codes: List[int] = None,
        error_codes: List[int] = None,
        response_model=None,
        actions: List[ResponseActions] = None,
        ignore_action_if: Callable = None,
        lazy_errors=True
):
    """
    :param success_codes: A list of success response codes that will
    be used to check if the current response code is in this list.
    If it is not included, then it will be considered as an error.
    For example if ``success_codes=[200, 201, 202]`` and response code
    is 400, then error will be raised.
    :param error_codes: List of error codes that describe what status
    response codes should be treated as errors.
    For example if ``error_codes=[400, 404, 500]`` and response code
    is 400, then error will be raised.
    :param response_model: The response model in the json representation that
    the current response must match.
    :param actions: List with enum ``ResponseActions`` of actions which we are
    going to execute for validation our response. For example it might look like
    ``actions=[ResponseActions.OK, ResponseActions.STATUS_CODE, ResponseActions.JSON]``
    :param ignore_action_if: Any callable object which can describe when we should ignore
    certain type of validation. For example if we need to test some negative scenario and
    we are EXPECTING that our function will return negative status code.
    ``ignore_action_if`` should look like:
    ```
        from requests import Response

        def my_custom_ignore_response(response: Response, action: str) -> bool:
            return (response.status_code == 400) and (action == 'json')
    ```
    :param lazy_errors: If ``True``, then each validation error will be added to generator
    object but not raised. All errors will be raised at once

    If ``False``, then first happened validation error will be raised immediately
    :return: ``Response`` requests object
    """

    def inner(func):
        def wrapper(*args, **kwargs):
            response: Response = func(*args, **kwargs)

            validator = ResponseValidator(
                response=response,
                func=func,
                error_codes=error_codes,
                success_codes=success_codes,
                response_model=response_model,
                actions=actions,
                ignore_action_if=ignore_action_if,
                lazy_errors=lazy_errors
            )

            with allure.step(f'Running validation for "{func.__name__}" response'):
                validator.raise_for_validation()

            return response

        return wrapper

    return inner
