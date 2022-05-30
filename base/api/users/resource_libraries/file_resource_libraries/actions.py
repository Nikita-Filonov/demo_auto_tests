from enum import Enum
from typing import Optional, Union, BinaryIO

import allure
from api_manager import post

from base.api.base import USERS_API_URL
from models.users.resource_library_files import ResourceLibraryFilePayload
from utils.api.utils import encode_to_url
from utils.formatters.api.file_resource_libraries import format_resource_library_storage_action
from utils.typing import PathLike


class ResourceLibrariesStorageAction(Enum):
    """
    Path for url action to work with certain type of objects in storage

    /api/v1/file-resource-libraries/{libraryId}/{action}/{path}
    """
    DIRECTORIES = 'directories'
    FILES = 'files'


def file_resource_libraries_action(
        action_type: ResourceLibrariesStorageAction,
        resource_library_id: str,
        storage_path: PathLike,
        payload: ResourceLibraryFilePayload,
        local_file: Optional[Union[BinaryIO, PathLike]] = None,
        user=None
):
    """
    :param action_type: Enum ``ResourceLibrariesStorageAction`` for action
    :param resource_library_id: Id of recourse library
    :param storage_path: Path to object in a bucket storage
    :param payload: ``ResourceLibraryFilePayload`` payload to send in form data.
    Must look like:
    {
        "type": 1,
        "jsonPayload": {
            "targetPath": "some/path"
        }
    }
    :param local_file: Path to file on local disk
    :param user: User to get token
    :return: ``Response`` object

    Wrapper around base API action for storage:
    - /api/v1/file-resource-libraries/{libraryId}/files/{path}
    - /api/v1/file-resource-libraries/{libraryId}/directories/{path}
    """
    json = payload.manager.to_json
    url = USERS_API_URL + f'/file-resource-libraries/{resource_library_id}' \
                          f'/{action_type.value}/{encode_to_url(storage_path)}'

    if (local_file is not None) and isinstance(local_file, str):
        with open(local_file, 'rb') as buffer_file:
            return post(url, files={'file': buffer_file}, data=json, user=user)

    return post(url, files={'file': local_file}, data=json, user=user)


def file_resource_libraries_file_action(
        resource_library_id: str,
        storage_path: PathLike,
        payload: ResourceLibraryFilePayload,
        local_file: Optional[Union[BinaryIO, PathLike]] = None,
        user=None
):
    """
    Wrapper around ``file_resource_libraries_action``, which adds
    allure step and ``action_type`` for files
    """
    step = format_resource_library_storage_action(
        action_type=ResourceLibrariesStorageAction.FILES,
        resource_library_id=resource_library_id,
        storage_path=storage_path,
        payload=payload,
        local_file=local_file
    )
    with allure.step(step):
        return file_resource_libraries_action(
            action_type=ResourceLibrariesStorageAction.FILES,
            resource_library_id=resource_library_id,
            storage_path=storage_path,
            payload=payload,
            local_file=local_file,
            user=user
        )


def file_resource_libraries_directory_action(
        resource_library_id: str,
        storage_path: PathLike,
        payload: ResourceLibraryFilePayload,
        local_file: Optional[Union[BinaryIO, PathLike]] = None,
        user=None
):
    """
    Wrapper around ``file_resource_libraries_action``, which adds
    allure step and ``action_type`` for directories
    """
    step = format_resource_library_storage_action(
        action_type=ResourceLibrariesStorageAction.DIRECTORIES,
        resource_library_id=resource_library_id,
        storage_path=storage_path,
        payload=payload,
        local_file=local_file
    )
    with allure.step(step):
        return file_resource_libraries_action(
            action_type=ResourceLibrariesStorageAction.DIRECTORIES,
            resource_library_id=resource_library_id,
            storage_path=storage_path,
            payload=payload,
            local_file=local_file,
            user=user
        )
