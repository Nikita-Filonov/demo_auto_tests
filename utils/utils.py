import functools
import logging
import math
import os
from mimetypes import guess_extension
from random import choice, randint
from string import ascii_letters, digits
from time import sleep
from typing import List, Dict, Union, Callable, Iterable, Optional, Any, Tuple, Type

import allure
from faker import Faker
from models_manager import Model
from models_manager.manager.model import Meta
from selenium.common.exceptions import WebDriverException
from waiting import wait as wait_lib

from settings import WAIT_TIMEOUT
from utils.ui.constants import DOWNLOAD_PATH

fake = Faker()
SIZE_NAMES = ("B", "KB", "MB", "GB",)


def random_string(start: int = 20, end: int = 50) -> str:
    """
    :param start:
    :param end:
    :return:
    """
    return ''.join(choice(ascii_letters + digits) for _ in range(randint(start, end)))


def random_number(start: int = 5, end: int = 50) -> int:
    return randint(start, end)


def random_dict(keys_count=5, types=(str, int, bool), **kwargs) -> dict:
    """
    :param keys_count: max number of keys that's will be in dictionary
    :param types: types that's will be in dictionary
    :param kwargs: additional settings which ``pydict`` takes
    :return: random dictionary
    """
    return fake.pydict(nb_elements=keys_count, value_types=types, **kwargs)


def random_list(elements=5, types=(str, int, bool), **kwargs):
    """
    :param elements: max number of elements that's will be in list
    :param types: types that's will be in list
    :param kwargs: additional settings which ``pylist`` takes
    :return: random list
    """
    return fake.pylist(nb_elements=elements, value_types=types, **kwargs)


def random_color() -> str:
    """Used to generate random color"""
    red = random_number(0, 255)
    green = random_number(0, 255)
    blue = random_number(0, 255)
    alpha = random_number(0, 255)
    return '#{:02x}{:02x}{:02x}{:02x}'.format(red, green, blue, alpha).upper()


def wait(*args, **kwargs):
    """
    Wrapping 'wait()' method of 'waiting' library with default parameter values.
    WebDriverException is ignored in the expected exceptions by default.
    """
    kwargs.setdefault('sleep_seconds', (1, None))
    kwargs.setdefault('expected_exceptions', WebDriverException)
    kwargs.setdefault('timeout_seconds', WAIT_TIMEOUT)

    return wait_lib(*args, **kwargs)


def retry(times, exceptions, delay=2):
    """
    Retry Decorator
    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown
    :param delay:
    :param times: The number of times to repeat the wrapped function/method
    :type times: Int
    :param exceptions: List or tuple of exceptions that trigger a retry attempt
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    logging.warning(
                        'Exception thrown when attempting to run %s, attempt '
                        '%d of %d' % (func, attempt, times)
                    )
                    attempt += 1
                sleep(delay)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def memoize(size: int = 2):
    """
    :param size: Size of cache. Meaning of this size depends on functions calls.
    :return:

    Caches function returning value up to "size".

    Example:

    @memoize(2)
    def my_function():
        return some_random_calculation()

    my_function() -> 'first_returned_value'
    my_function() -> 'first_returned_value'

    We call function two times, and how cache is full.
    Next call cache will be cleaned and function will be called again.

    my_function() -> 'second_returned_value'
    """
    cache = {}

    def inner(func):
        def wrapper(*args, **kwargs):
            if func in cache:

                if len(cache[func]) < size:
                    cache[func] = [*cache[func], cache[func][0]]
                    return cache[func][0]

            result = func(*args, **kwargs)
            cache[func] = [result]
            return result

        return wrapper

    return inner


def modify_list_of_dicts(list_of_dicts: List[Dict], key, value) -> List[Dict]:
    """
    Used to modify key/value in list of dicts

    Example:
    methods = [{'method': <some_function>, 'args': (1,2)}]
    modify_methods_response(methods, 400) -> [{'method': <some_function>, 'args': (1,2), 'response': 400}]
    """
    return [{**dictionary, key: value} for dictionary in list_of_dicts]


def check_downloaded_file(file_name: str):
    """Common method to check is file downloaded correctly"""
    with allure.step(f'Checking that file "{file_name}" exists and correct'):
        file_path = os.path.join(DOWNLOAD_PATH, file_name)
        logging.info(f'Checking file "{file_name}" in {file_path}')

        wait(lambda: os.path.exists(file_path), waiting_for=f'Until file "{file_name}" exists in {file_path}')
        assert os.path.isfile(file_path), f'Checking if "{file_path}" is correct file'


def file_name_or_path_resolve(file_path_or_name: str):
    """
    Should be used for resolve file name from file path/file

    Examples:
        file_name_or_path_resolve('some/path/any.png') -> any.png
        file_name_or_path_resolve('any.png') -> any.png
    """
    safe_file_name = file_path_or_name

    if os.path.isfile(file_path_or_name):
        safe_file_name = os.path.basename(file_path_or_name)

    return safe_file_name


def find(func: Callable, iterable: Iterable, default: Optional[Any] = None) -> Any:
    """
    :param func: Any callable
    :param iterable: Any iterable
    :param default: Default to return
    :return: Any result

    Wrapper around filter function that will return first founded value or default
    """
    return next((filter(lambda item: func(item), iterable)), default)


def unwrap(func: Callable) -> Callable:
    """Used to dynamically unwrap function"""
    if hasattr(func, '__wrapped__'):
        return func.__wrapped__

    return func


def to_pascal_case(string: str) -> str:
    """
    :param string: String in camel case 'someOther', 'other'
    :return: String in pascal case

    Examples:
        >>> to_pascal_case('other')
        'Other'
        >>> to_pascal_case('someOther')
        'SomeOther'
    """
    return string[0].upper() + string[1:]


def cache_callable(func: Callable) -> Callable:
    """
    :param func: Any callable object
    :return: Cached function

    Will cache returned value of callable object

    Examples:
        >>> from models_manager.utils import random_string
        >>> cached = cache_callable(random_string)
        >>> assert cached() == cached()
    """
    return functools.lru_cache(maxsize=None)(func)


def call(functions: Union[List[Callable], Tuple[Callable], Callable, Type[Model]]) -> Any:
    """
    :param functions: Any callable object or list of callable objects
    :return: Any object

    >>> call(lambda: 1)
    1
    >>> call([lambda: 1, lambda: 2])
    (1, 2)
    """
    if type(functions) == Meta:
        return functions.manager.to_json

    if not isinstance(functions, (list, tuple)):
        return functions() if callable(functions) else functions

    return tuple(call(func) for func in functions)


def get_file_size(size: int) -> str:
    """
    Get file size with unit ism in format for Alert message
    Example:
        get_file_size(30000) -> '29 KB'
        get_file_size(3000000) -> '2,9 MB'
    """
    if size == 0:
        return "0 B"

    size_name_index = int(math.floor(math.log(size, 1024)))
    byte_to_the_power = math.pow(1024, size_name_index)
    converted_size = round(size / byte_to_the_power, None if size < 1000 * 1024 else 1)
    return "%s %s" % (converted_size, SIZE_NAMES[size_name_index])


def get_extensions_from_mime(mime_types: Union[str, list, tuple], ignore_empty=True) -> List[Union[str, None]]:
    """
    :param mime_types: Should be list or tuple of mime types or string. If mime types is
    a string, then we expecting something like this 'application/json,text/html,image/png'.
    :param ignore_empty: If True, then all underfunded extensions will be remove from the result list.
    If False, then underfunded extensions will be not remove from the result list.
    :return: Will return list of extensions

    Example:
        get_extensions_from_mime('image/png,application/msword') -> ['.png', '.doc']
        get_extensions_from_mime(['image/png', 'application/msword']) -> ['.png', '.doc']
    """
    if isinstance(mime_types, str):
        mime_types = mime_types.split(',')

    extensions = [guess_extension(mime_type) for mime_type in mime_types]

    if not ignore_empty:
        return extensions

    return list(filter(None, extensions))


def deep_get(dictionary: dict, *keys):
    """
    Used to get nested keys from the ``dictionary`` dynamically

    Examples:
        >>> some_dict = {'user': {'id': 1}}
        >>> deep_get(some_dict, 'user', 'id')
        1

        >>> some_dict = {'user': {'id': {'value': 'some value'}}}
        >>> deep_get(some_dict, 'user', 'id', 'value')
        'some value'
    """
    return functools.reduce(lambda d, key: d.get(key) if d else None, keys, dictionary)
