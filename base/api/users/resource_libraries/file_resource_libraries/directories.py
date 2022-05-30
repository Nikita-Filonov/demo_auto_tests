import json as json_lib

import allure

from base.api.users.resource_libraries.file_resource_libraries.actions import file_resource_libraries_directory_action
from models.users.resource_library_files import ResourceLibraryFilePayload, SupportedResourceLibraryFileActions, \
    ResourceLibraryFileJsonPayload


def create_resource_library_directory(resource_library_id, storage_path, user=None):
    with allure.step(f'Creating directory "{storage_path}" for resource library with id "{resource_library_id}"'):
        payload = ResourceLibraryFilePayload(type=SupportedResourceLibraryFileActions.CREATING_FILE.value)
        return file_resource_libraries_directory_action(
            resource_library_id=resource_library_id,
            storage_path=storage_path,
            payload=payload,
            user=user
        )


def delete_resource_library_directory(resource_library_id, storage_path, user=None):
    with allure.step(f'Deleting directory "{storage_path}" for resource library with id "{resource_library_id}"'):
        payload = ResourceLibraryFilePayload(type=SupportedResourceLibraryFileActions.DELETE_FILE.value)
        return file_resource_libraries_directory_action(
            resource_library_id=resource_library_id,
            storage_path=storage_path,
            payload=payload,
            user=user
        )


def move_resource_library_directory(
        resource_library_id,
        storage_path,
        json_payload: ResourceLibraryFileJsonPayload,
        user=None
):
    with allure.step(f'Moving directory from "{storage_path}" to "{json_payload.target_path.value}" '
                     f'for resource library with id "{resource_library_id}"'):
        payload = ResourceLibraryFilePayload(
            type=SupportedResourceLibraryFileActions.MOVE_FILE.value,
            jsonPayload=json_lib.dumps(json_payload.manager.to_json)
        )
        return file_resource_libraries_directory_action(
            resource_library_id=resource_library_id,
            storage_path=storage_path,
            payload=payload,
            user=user
        )
