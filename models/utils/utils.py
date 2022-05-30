import logging
import os
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Optional

from settings import DEBUG, MINIO_FOLDER
from utils.api.constants import DEFAULT_TEXTBOOK_ATTACHMENT_PATH
from utils.minio.storage import upload_to_storage
from utils.utils import random_string, random_number, memoize

logging.basicConfig(level=logging.INFO)


def filter_scopes(permissions, scope=None, *args):
    """
    :param scope:
    :param permissions:
    :param args:
    :return:
    """
    if not args:
        return permissions

    return list(
        filter(
            lambda perm: any((arg in perm['name']) and (perm['scope'] == scope) for arg in args),
            permissions
        )
    )


def get_email(domain='@gmail.com'):
    """Used to get random email"""
    return random_string() + domain


def get_date(delta_hours: int = 3) -> datetime:
    """
    Used to get current date depends on environment.

    If DEBUG = True - we guess that currently autotests running locally,
    so we are using datetime.now().

    If DEBUG = False - we guess that currently autotests running inside
    Docker container and timezone might be different from current,
    so we are using datetime.now() + timedelta(hours=<delta_hours>)
    """
    return datetime.now() if DEBUG else datetime.now() + timedelta(hours=delta_hours)


def get_code():
    """Activity/Objective code"""
    return random_string(5, 15)


def get_min_bonus():
    """Element min bonus value"""
    return random_number(-50, 0)


@memoize(2)
def get_tool_resource_id():
    """
    :return: Resource element id

    Implements logic of https://youtrack.alemira.dev/issue/ALMS-1296
    So we are unable to cache/use same activity + resource for different activities.

    Also we should use same resource for toolUrl, toolResourceId. For that
    we are using memoize with size equal 2
    """
    from models.ztool.element import get_default_element  # noqa
    return get_default_element()


@contextmanager
def clear_log(model):
    model_name = model.__name__
    logging.info(f'Starting to clear "{model_name}"')
    yield
    logging.info(f'"{model_name}" successfully cleared\n')


def get_attachment_name(file_name_or_path: Optional[str] = None):
    """
    Used to get attachment name with random name.

    By default used random file name and '.pdf' extension.
    If you want to override extension, then pass ``file_name_or_path``
    with needed extension.
    """
    file_extension = '.pdf'
    if file_name_or_path is not None:
        _, file_extension = os.path.splitext(file_name_or_path)

    return random_string() + file_extension


def get_default_textbook_url(file_name: Optional[str] = None):
    """
    Wrapper around ``upload_to_storage`` for uploading
    default textbook attachment with random name
    """
    safe_file_name = file_name or get_attachment_name()
    return upload_to_storage(DEFAULT_TEXTBOOK_ATTACHMENT_PATH, f'{MINIO_FOLDER}/{safe_file_name}')
