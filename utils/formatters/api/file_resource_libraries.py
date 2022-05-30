from typing import Optional, Union, BinaryIO

from models.users.resource_library_files import ResourceLibraryFilePayload
from utils.typing import PathLike


def format_resource_library_storage_action(
        action_type,
        resource_library_id: str,
        storage_path: PathLike,
        payload: ResourceLibraryFilePayload,
        local_file: Optional[Union[BinaryIO, PathLike]],
):
    return f'Making action for {action_type.value}. Properties:\n' \
           f'Resource library id: "{resource_library_id}"\n' \
           f'Storage path: "{storage_path}"\n' \
           f'Action Type: "{payload.type.value}"\n' \
           f'Json payload: "{payload.json_payload.value}"\n' \
           f'Local file: "{local_file}"'
