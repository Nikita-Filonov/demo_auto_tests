from typing import Tuple

import pytest

from base.api.users.resource_libraries.file_resource_libraries.directories import create_resource_library_directory
from base.api.users.resource_libraries.file_resource_libraries.files import upload_resource_library_file
from base.api.users.resource_libraries.resource_libraries import create_resource_library
from models.users.resource_libraries import ResourceLibraries, ResourceLibrariesLTI13
from utils.assertions.files import assert_file_exists_in_bucket_folder
from utils.minio.utils import safe_storage_path
from utils.typing import PathLike


@pytest.fixture(scope='function')
def resource_library(request) -> Tuple[ResourceLibraries, dict]:
    """
    For creating resource library with type based on library_model
    Default model is ResourceLibrariesLTI13
    """

    library_model: ResourceLibraries = request.param if hasattr(request, 'param') else ResourceLibrariesLTI13
    resource_library_payload = library_model.manager.to_json
    return library_model, create_resource_library(resource_library_payload).json()


@pytest.fixture(scope='function')
def resource_library_with_file(request, resource_library) -> dict:
    _, resource_library = resource_library

    if not hasattr(request, 'param'):
        raise NotImplementedError('')

    params = request.param
    upload_resource_library_file(resource_library_id=resource_library['id'], **params)

    assert_file_exists_in_bucket_folder(params['storage_path'])
    return params


@pytest.fixture(scope='function')
def resource_library_with_directory(request, resource_library) -> Tuple[PathLike, dict]:
    _, resource_library = resource_library

    if not hasattr(request, 'param'):
        raise NotImplementedError('')

    directory = safe_storage_path(**request.param)
    create_resource_library_directory(resource_library['id'], directory)

    return directory, resource_library
