import os
from typing import Optional

from settings import MINIO_FOLDER
from utils.typing import PathLike


def safe_storage_path(file_name_or_path: PathLike) -> PathLike:
    """
    :param file_name_or_path: Any file or path string.
    For example '/some/path/to/file.png', '/some/path/to/'.
    :return: Will return safe storage path, which is pointed
    to autotests folder

    Example:
        >>> safe_storage_path('/some/path/to/')
        'autotests/some/path/to/'
        >>> safe_storage_path('some/path/to/')
        'autotests/some/path/to/'

        >>> safe_storage_path('/some/path/to/my.png')
        'autotests/some/path/to/my.png'
        >>> safe_storage_path('some/path/to/my.png')
        'autotests/some/path/to/my.png'
    """
    if not file_name_or_path.startswith(MINIO_FOLDER):
        safe_file_name_or_path = file_name_or_path if file_name_or_path.startswith('/') else ('/' + file_name_or_path)
        file_name_or_path = MINIO_FOLDER + safe_file_name_or_path

    return file_name_or_path


def switch_file_name(
        base_path: PathLike,
        new_file_name: Optional[PathLike] = None,
        new_path: Optional[PathLike] = None
) -> PathLike:
    """
    :param base_path: Base path from which we can extract file name, extension
    :param new_path: New path which we want to use
    :param new_file_name: New file name which want to use
    :return: Switched file path

    Example:
        >>> switch_file_name('/some/path/to/my.png', new_path='/other/path/')
        'autotests/other/path/my.png'
        >>> switch_file_name('/some/path/to/my.png', new_path='/other/path/', new_file_name='other')
        'autotests/other/path/other.png'
        >>> switch_file_name('/some/path/to/my.png', new_file_name='other')
        'autotests/other.png'
        >>> switch_file_name('/some/path/to/my.png')
        'autotests/my.png'
    """
    safe_path = safe_storage_path(new_path or '')

    _, file_extension = os.path.splitext(base_path)
    original_file_name = os.path.basename(base_path)

    if new_file_name is None:
        return safe_path + original_file_name

    return safe_path + new_file_name + file_extension
