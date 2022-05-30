import json as json_lib

import allure

from base.api.users.resource_libraries.file_resource_libraries.actions import file_resource_libraries_file_action
from models.users.resource_library_files import ResourceLibraryFilePayload, SupportedResourceLibraryFileActions, \
    ResourceLibraryFileJsonPayload


def upload_resource_library_file(resource_library_id, storage_path, local_file=None, user=None):
    with allure.step(f'Uploading file in storage path "{storage_path}" '
                     f'to resource library with id "{resource_library_id}"'):
        payload = ResourceLibraryFilePayload(Type=SupportedResourceLibraryFileActions.CREATING_FILE.value)
        return file_resource_libraries_file_action(
            resource_library_id=resource_library_id,
            storage_path=storage_path,
            local_file=local_file,
            payload=payload,
            user=user
        )


def delete_resource_library_file(resource_library_id, storage_path, user=None):
    with allure.step(f'Deleting file from storage path "{storage_path}" '
                     f'for resource library with id "{resource_library_id}"'):
        payload = ResourceLibraryFilePayload(type=SupportedResourceLibraryFileActions.DELETE_FILE.value)
        return file_resource_libraries_file_action(
            resource_library_id=resource_library_id,
            storage_path=storage_path,
            payload=payload,
            user=user
        )


def move_resource_library_file(
        resource_library_id,
        storage_path,
        json_payload: ResourceLibraryFileJsonPayload,
        user=None
):
    with allure.step(f'Moving file from path "{storage_path}" to path "{json_payload.target_path.value}" '
                     f'for resource library with id "{resource_library_id}"'):
        payload = ResourceLibraryFilePayload(
            type=SupportedResourceLibraryFileActions.MOVE_FILE.value,
            jsonPayload=json_lib.dumps(json_payload.manager.to_json)
        )
        return file_resource_libraries_file_action(
            resource_library_id=resource_library_id,
            storage_path=storage_path,
            payload=payload,
            user=user
        )


def get_resource_library_file_download_link(resource_library_id, storage_path, user=None):
    with allure.step(f'Getting download link to file in storage path "{storage_path}" '
                     f'for resource library with id "{resource_library_id}"'):
        payload = ResourceLibraryFilePayload(type=SupportedResourceLibraryFileActions.DOWNLOAD_FILE.value)
        return file_resource_libraries_file_action(
            resource_library_id=resource_library_id,
            storage_path=storage_path,
            payload=payload,
            user=user
        )
