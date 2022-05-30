import logging
import os
from http import HTTPStatus

import allure
from assertions import assert_response_status

from settings import MINIO_PRIVATE_BUCKET_NAME
from utils.minio.storage import get_file_in_folder
from utils.ui.constants import DOWNLOAD_PATH
from utils.utils import wait


def assert_downloaded_file(file_name: str):
    """Common method to check is file downloaded correctly"""
    with allure.step(f'Checking that file "{file_name}" exists and correct'):
        file_path = os.path.join(DOWNLOAD_PATH, file_name)
        logging.info(f'Checking file "{file_name}" in {file_path}')

        wait(lambda: os.path.exists(file_path), waiting_for=f'Until file "{file_name}" exists in {file_path}')
        assert os.path.isfile(file_path), f'Checking if "{file_path}" is correct file'


def assert_file_exists_in_bucket_folder(path: str):
    """
    :param path: Any path string which we want to check in our bucket
    :raises: AssertionError if file does not exists
    """
    with allure.step(f'Checking that file "{path}" exists in a bucket "{MINIO_PRIVATE_BUCKET_NAME}"'):
        file = get_file_in_folder(object_name=path)

        assert file, f'Unable to find file "{path}" in a bucket "{MINIO_PRIVATE_BUCKET_NAME}"'
        assert_response_status(file.status, HTTPStatus.OK)


def assert_file_does_not_exists_in_bucket_folder(path: str):
    """
    :param path: Any path string which we want to check in our bucket
    :raises: AssertionError if file does exists
    """
    with allure.step(f'Checking that file "{path}" does not exists in a bucket "{MINIO_PRIVATE_BUCKET_NAME}"'):
        file = get_file_in_folder(object_name=path)

        assert file is None, f'File "{path}" was found in a bucket "{MINIO_PRIVATE_BUCKET_NAME}"'
