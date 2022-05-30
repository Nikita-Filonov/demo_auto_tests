from typing import Union, Callable, Dict

import allure

from utils.api.users.common import Endpoint


def to_sentence(method: Union[Callable, object]):
    """
    Can be used to extract method/object name and convert
    it to human readable representation

    Example:
        >>> def my_function():
        ...     ...
        ...
        >>> to_sentence(my_function)
        'My function'
    """
    sentence = ' '.join(method.__name__.split('_'))
    return sentence[:1].upper() + sentence[1:]


def to_method_param(func: Union[Endpoint, Dict[str, Union[Callable, str, tuple]]]):
    """
    Can be used for autotests with method parametrization, to
    override default pytest parametrization suffix.
    And to add description of action that was made
    """
    if isinstance(func, dict):
        func = func['method']

    if isinstance(func, Endpoint):
        func = func.method

    allure.dynamic.description(f'Action: {to_sentence(func)}')
    return func.__name__
