import os
from typing import List, Tuple

import allure
from assertions import assert_truth, validate_json, assert_model_equal, assert_not_truth

from base.api.users.resource_libraries.resource_libraries import get_resource_library_resources_in_path
from models.users.resource_library_files import RecourseLibraryResource, RecourseLibraryResourceTypes
from settings import MINIO_FOLDER
from utils.typing import PathLike
from utils.utils import find


def get_path_to_resource_in_storage(storage_path: PathLike) -> Tuple[str, PathLike]:
    """
    :param storage_path: Some path to resource in storage. For example autotests/some/my.png
    :return: Will return file name and path to file without ``MINIO_FOLDER``

    Examples:
        >>> get_path_to_resource_in_storage('autotests/some/my.png')
        ('my.png', '/some')
        >>> get_path_to_resource_in_storage('autotests/some/other/my.png')
        ('my.png', '/some/other')
    """
    file_name = os.path.basename(storage_path)
    return file_name, storage_path.replace(MINIO_FOLDER, '').replace(f'/{file_name}', '')


def find_resource(resource_id: str, resources: List[dict]) -> dict:
    """
    :param resource_id: Library resource id
    :param resources: List of library resources
    :return: Library resource object
    """
    with allure.step(f'Finding resource with id "{resource_id}"'):
        file_to_check = find(lambda f: f['id'] == resource_id, resources, default=None)

    assert_truth(file_to_check, 'Resource of resource library')
    return file_to_check


def ensure_user_can_view_file(resource_library_id: str, storage_path: PathLike, local_file: PathLike, user=None):
    """
    :param resource_library_id: Library id
    :param storage_path: Path to file in storage bucket
    :param local_file: Path to file on local disk
    :param user: User object
    :raises: ``AssertionError``, ``jsonschema.exceptions.ValidationError``

    Used to ensure that library resource file was uploaded to storage
    and user can view this resource

    Also will ensure that resource is shown correctly
    """
    file_size = os.path.getsize(local_file)
    file_name = os.path.basename(storage_path)
    _, file_extension = os.path.splitext(storage_path)
    path_to_file = storage_path.replace(file_name, '')

    with allure.step(f'Ensure user can view file "{storage_path}" resource'):
        files = get_resource_library_resources_in_path(resource_library_id, path_to_file, user=user).json()
        file_to_check = find_resource(storage_path, files)

        expected_file_resource = RecourseLibraryResource(
            id=storage_path,
            path=storage_path,
            name=file_name,
            size=file_size,
            type=file_extension[1:]
        ).manager.to_dict()

        validate_json(json=files, schema=RecourseLibraryResource.manager.to_array_schema)
        assert_model_equal(
            left=file_to_check,
            right=expected_file_resource,
            model=RecourseLibraryResource,
            exclude=[RecourseLibraryResource.modified.json]
        )


def ensure_user_can_view_directory(resource_library_id: str, storage_path: PathLike, user=None):
    """
    :param resource_library_id: Library id
    :param storage_path: Path to file in storage bucket
    :param user: User object
    :raises: ``AssertionError``, ``jsonschema.exceptions.ValidationError``

    Used to ensure that library resource directory was created in storage
    and user can view this resource

    Also will ensure that resource is shown correctly
    """
    file_name, path_to_directory = get_path_to_resource_in_storage(storage_path)
    absolute_storage_path = storage_path.replace(f'/{file_name}', '')
    recourse_id = f'{absolute_storage_path}/'

    with allure.step(f'Ensure user can view directory "{storage_path}" resource'):
        directories = get_resource_library_resources_in_path(
            resource_library_id, absolute_storage_path, user=user).json()
        directory_to_check = find_resource(recourse_id, directories)

        expected_directory_resource = RecourseLibraryResource(
            id=recourse_id,
            path=recourse_id,
            name=path_to_directory.split('/')[-1],
            type=RecourseLibraryResourceTypes.DIRECTORY.value
        ).manager.to_dict()

        validate_json(json=directories, schema=RecourseLibraryResource.manager.to_array_schema)
        assert_model_equal(directory_to_check, expected_directory_resource, RecourseLibraryResource)


def ensure_user_can_not_view_directory(resource_library_id: str, storage_path: PathLike, user=None):
    """
    :param resource_library_id: Library id
    :param storage_path: Path to file in storage bucket
    :param user: User object
    :raises: ``AssertionError``

    Used to ensure that user can not view directory
    """
    _, path_to_directory = get_path_to_resource_in_storage(storage_path)

    with allure.step(f'Ensure user can not view directory "{storage_path}" resource'):
        directories = get_resource_library_resources_in_path(resource_library_id, path_to_directory, user=user).json()
        assert_not_truth(directories, what=f'Resource library directory')
