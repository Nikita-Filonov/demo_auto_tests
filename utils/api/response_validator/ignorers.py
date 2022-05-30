from http import HTTPStatus

from requests import Response

from utils.api.response_validator.actions import ResponseActions


def ignore_unauthorized(response: Response, action: str) -> bool:
    """Used to ignore json validation action when response status code is ``UNAUTHORIZED``"""
    return (action == ResponseActions.JSON.value) and (response.status_code == HTTPStatus.UNAUTHORIZED)
