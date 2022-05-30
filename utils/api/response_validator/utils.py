from http import HTTPStatus
from typing import List, Union


def join_errors(codes: List[int]) -> str:
    """
    :param codes: List with integer codes numbers
    :return: Codes joined into string

    Examples:
        >>> join_errors([200, 400, 500])
        '200, 400, 500'
    """
    return ', '.join(map(str, codes))


def safe_codes(codes: Union[List[int], List[HTTPStatus]]) -> List[int]:
    """
    :return: List with integer codes numbers

    Used to extract value from ``_error_codes``, which can be just number
    or Enum object

    Examples:
        >>> safe_codes([HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.BAD_REQUEST])
        [200, 202, 400]
    """
    return [(error.value if hasattr(error, 'value') else error) for error in codes]
