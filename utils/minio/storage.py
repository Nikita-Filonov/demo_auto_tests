import logging
import os
from typing import Optional, List, Union

from minio import S3Error
from minio.datatypes import Object
from minio.deleteobjects import DeleteObject, DeleteError
from urllib3 import HTTPResponse

from settings import MINIO_FOLDER, MINIO_PRIVATE_BUCKET_NAME
from utils.minio.client import storage_client


def create_bucket(bucket_name: Optional[str] = MINIO_PRIVATE_BUCKET_NAME):
    """
    Should be used to check if s3 bucket with name ``bucket_name`` exists.
    If such does not exits then this method will create it.
    """
    bucket = storage_client.bucket_exists(bucket_name)
    logging.info(f'Checking if bucket "{bucket_name}" already exists')

    if not bucket:
        logging.info(f'Bucket "{bucket_name}" does not exists')
        storage_client.make_bucket(bucket_name)
        logging.info(f'Bucket "{bucket_name}" successfully created')
    else:
        logging.info(f'Bucket "{bucket_name}" already exists')


def upload_to_storage(file_path: str, file_name: Optional[str] = None, bucket_name: Optional[str] = MINIO_PRIVATE_BUCKET_NAME):
    """
    Should be used to upload file to s3 storage.

    Will return uri of uploaded file

    Example:
        upload_to_storage('parameters/files/some.png') -> 'https://host.docker.internal:9000/some.uri.some.png'
    """
    if file_name is None:
        file_name = f'{MINIO_FOLDER}/{os.path.basename(file_path)}'

    storage_client.fput_object(bucket_name, file_name, file_path)
    logging.info(f'Successfully uploaded "{file_path}" to storage')

    uri = storage_client.presigned_get_object(bucket_name, file_name)
    logging.info(f'Uri of uploaded file: {uri}')
    return uri


def remove_files_from_storage(
        objects: List[Object],
        bucket_name: Optional[str] = MINIO_PRIVATE_BUCKET_NAME
) -> List[DeleteError]:
    """
    :param objects: List of ``minio.datatypes.Object`` objects
    :param bucket_name: Optional bucket name. If no bucket name provided, then
    default ``MINIO_PRIVATE_BUCKET_NAME`` will be used.
    :return: List of ``minio.deleteobjects.DeleteObject`` objects

    Can be used to remove multiple objects from storage

    Reference https://github.com/minio/minio-py/blob/master/examples/remove_objects.py
    """
    delete_objects = [DeleteObject(obj.object_name) for obj in objects]
    logging.info(f'Starting to deleting {len(delete_objects)} files from storage')

    errors = list(storage_client.remove_objects(bucket_name=bucket_name, delete_object_list=delete_objects))
    logging.info(f'Successfully deleted {len(delete_objects) - len(errors)} files from storage')
    return errors


def get_files_in_folder(
        folder: Optional[str] = MINIO_FOLDER,
        bucket_name: Optional[str] = MINIO_PRIVATE_BUCKET_NAME
) -> List[Object]:
    """
    :param folder: Optional folder name. If no folder provided default
    autotests ``MINIO_FOLDER`` will be used.
    :param bucket_name: Optional bucket name. If no bucket name provided, then
    default ``MINIO_PRIVATE_BUCKET_NAME`` will be used.
    :return: List of ``minio.datatypes.Object`` objects

    Reference https://github.com/minio/minio-py/blob/master/examples/list_objects.py
    """
    logging.info(f'Getting all files in folder "{folder}"')

    files = list(storage_client.list_objects(bucket_name=bucket_name, prefix=f'{folder}/'))
    logging.info(f'Found {len(files)} files in the folder "{folder}"')
    return files


def get_file_in_folder(
        object_name: str,
        file_path: str = None,
        bucket_name: Optional[str] = MINIO_PRIVATE_BUCKET_NAME
) -> Union[HTTPResponse, None]:
    """
    :param object_name: Object name in a folder
    :param file_path: File path on local disk. If provided,
    then file will be saved to this file
    :param bucket_name: Optional bucket name. If no bucket name provided, then
    default ``MINIO_PRIVATE_BUCKET_NAME`` will be used.
    :return: Will return file ``HTTPResponse`` if file exists in bucket.
    If file does not exists then will return ``None``

    Reference https://github.com/minio/minio-py/blob/master/examples/get_object.py,
    https://github.com/minio/minio-py/blob/master/examples/fget_object.py
    """
    try:
        response = storage_client.get_object(bucket_name=bucket_name, object_name=object_name)
    except S3Error:
        return

    if file_path is not None:
        storage_client.fget_object(bucket_name=bucket_name, object_name=object_name, file_path=file_path)

    response.close()
    response.release_conn()

    return response
