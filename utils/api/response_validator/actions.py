from enum import Enum


class ResponseActions(Enum):
    """
    Actions which can be provided to ``ResponseValidator`` to
    validate certain actions of response.
    """
    STATUS_CODE = 'status_code'
    OK = 'ok'
    JSON = 'json'
    RESPONSE_MODEL = 'response_model'
