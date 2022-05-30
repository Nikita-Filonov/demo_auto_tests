from typing import Optional

from models_manager import Model, Field, FieldGenericEnum


class SupportedResourceLibraryFileActions(FieldGenericEnum):
    MOVE_FILE = 1
    DELETE_FILE = 2
    DOWNLOAD_FILE = 3
    CREATING_FILE = 4
    UPDATING_FILE = 5


class RecourseLibraryResourceTypes(FieldGenericEnum):
    DIRECTORY = 'directory'


class ResourceLibraryFileJsonPayload(Model):
    target_path = Field(json='targetPath', category=str)


class ResourceLibraryFilePayload(Model):
    type = Field(
        json='type',
        default=SupportedResourceLibraryFileActions.CREATING_FILE.value,
        choices=SupportedResourceLibraryFileActions.to_list(),
        category=int
    )
    json_payload = Field(json='jsonPayload', category=str, null=True)


class RecourseLibraryDownloadFile(Model):
    url = Field(json='url', category=str)


class RecourseLibraryResource(Model):
    id = Field(json='id', category=str)
    path = Field(json='path', category=str)
    name = Field(json='name', category=str)
    modified = Field(json='modified', category=str, default='0001-01-01T00:00:00')
    size = Field(json='size', category=Optional[int], is_related=True, optional=True)
    type = Field(json='type', category=str)
