from http import HTTPStatus

from utils.api.response_validator.actions import ResponseActions

ERROR_CODES = [
    HTTPStatus.METHOD_NOT_ALLOWED,
    HTTPStatus.INTERNAL_SERVER_ERROR,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.GATEWAY_TIMEOUT
]
VALIDATOR_ACTIONS = [ResponseActions.STATUS_CODE, ResponseActions.JSON]
