from typing import Tuple

from settings import MINIO_PUBLIC_BUCKET_NAME, MINIO_HOST
from utils.utils import file_name_or_path_resolve


def get_element_file_url(element_id: str, file_name_or_path: str) -> Tuple[str, str]:
    """
    :param element_id: Identity of model models.ztool.Elements
    :param file_name_or_path: path to the file or file name
    :return: tuple with file name and url to file in storage

    Example:
        >>> get_element_file_url('some_id', 'some.png')
        ('some.png', 'https://host.docker.internal:9000/minio_public_bucket_name/elements/some_id/textbook/some.png')
    """
    safe_file_name = file_name_or_path_resolve(file_name_or_path)
    return safe_file_name, f'https://{MINIO_HOST}/{MINIO_PUBLIC_BUCKET_NAME}/elements/{element_id}/textbook/{safe_file_name}'
