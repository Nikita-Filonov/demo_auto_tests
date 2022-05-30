import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

from models_manager import Field, Model, FieldGenericEnum

from base.api.users.resource_libraries.resource_libraries import create_resource_library
from settings import DEFAULT_TENANT, USERS_DB_NAME, LAB_APPLICATION_USER, IDENTITY_SERVER, Z_TOOL_API, \
    MINIO_PRIVATE_BUCKET_NAME, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_HOST
from utils.utils import random_string


class SupportedResourceLibraryType(FieldGenericEnum):
    """ Supported Types for Resource Libraries """
    LTI_1_3 = 1
    PUBLIC_FILE = 2
    PRIVATE_FILE = 3
    LTI_1_1 = 4
    TEXT = 5
    COMPOSITE = 6


class ResourceLibraries(Model):
    """
    Base Model for Resource Library.
    Set general settings for different resource libraries types.
    To use one particular model, the settings with default=None must be overridden depending on the model.

    Example to overridden setting:

    type = Field(default=None, json='type', category=int) ->
    -> type = Field(default=SupportedResourceLibraryType.LTI_1_3.value, json='type', category=int)

    secret_key = Field(default=None, null=True, only_json=True, json='secretKey', category=str) ->
    -> secret_key = Field(default=random_string, null=True, only_json=True, json='secretKey', category=str)
    """

    SCOPE = [
        {'name': 'ResourceLibrary.Read', 'scope': None, 'scopeType': None},
        {'name': 'ResourceLibrary.Delete', 'scope': None, 'scopeType': None},
        {'name': 'ResourceLibrary.Update', 'scope': None, 'scopeType': None},
        {'name': 'ResourceLibrary.Create', 'scope': None, 'scopeType': None},
    ]
    database = USERS_DB_NAME
    identity = 'resource_library_id'

    resource_library_id = Field(default=uuid.uuid4, json='id', category=str)
    tenant_id = Field(default=DEFAULT_TENANT['id'], is_related=True, category=str)
    name = Field(default=random_string, json='name', category=str)
    application_id = Field(default=uuid.uuid4, category=str)
    image_url = Field(default=random_string, null=True, only_json=True, json='imageUrl', category=str)
    type = Field(json='type', category=int, choices=SupportedResourceLibraryType.to_list())
    url = Field(default=Z_TOOL_API + '/api/v1/elements', null=True, json='url', category=str)
    action_api_url = Field(null=True, only_json=True, json='actionsApiUrl', category=Optional[str])
    support_lti_review = Field(null=True, json='supportLtiReview', category=Optional[bool])
    support_lti_grading = Field(null=True, json='supportLtiGrading', category=Optional[bool])
    support_lti_authoring = Field(null=True, json='supportLtiAuthoring', category=Optional[bool])
    bucket_name = Field(null=True, json='bucketName', category=Optional[str])
    subfolder = Field(null=True, json='subfolder', category=Optional[str])
    user = Field(default=LAB_APPLICATION_USER['user'], null=True, json='user', category=Optional[str])
    password = Field(default=LAB_APPLICATION_USER['password'], null=True, json='password', category=Optional[str])
    allow_publishing = Field(default=False, json='allowPublishing', category=bool)
    allow_editing = Field(default=False, json='allowEditing', category=bool)
    consumer_key = Field(null=True, json='consumerKey', category=Optional[str])
    secret_key = Field(null=True, json='secretKey', category=Optional[str])
    auth_url = Field(null=True, json='authUrl', category=Optional[str])
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    created_on_behalf_of_user_id = Field(default=uuid.uuid4, category=str)
    modified = Field(null=True, category=str)
    modified_by_user_id = Field(null=True, category=str)
    modified_on_behalf_of_user_id = Field(null=True, category=str)
    removed = Field(null=True, category=str)
    removed_by_user_id = Field(null=True, category=str)
    removed_on_behalf_of_user_id = Field(null=True, category=str)

    def __str__(self):
        return f'<ResourceLibraries {self.resource_library_id}, {self.name}>'


class ResourceLibrariesLTI13(ResourceLibraries):
    extended_by = ResourceLibraries

    type = Field(default=SupportedResourceLibraryType.LTI_1_3.value, json='type', category=int)
    action_api_url = Field(
        default=Z_TOOL_API + '/api/v1/actions',
        null=True,
        only_json=True,
        json='actionsApiUrl',
        category=Optional[str]
    )
    support_lti_review = Field(default=False, null=True, json='supportLtiReview', category=Optional[bool])
    support_lti_grading = Field(default=False, null=True, json='supportLtiGrading', category=Optional[bool])
    support_lti_authoring = Field(default=False, null=True, json='supportLtiAuthoring', category=Optional[bool])
    auth_url = Field(default=IDENTITY_SERVER, null=True, json='authUrl', category=Optional[str])


class ResourceLibrariesLTI11(ResourceLibraries):
    extended_by = ResourceLibraries

    type = Field(default=SupportedResourceLibraryType.LTI_1_1.value, json='type', category=int)
    action_api_url = Field(default=random_string, null=True, json='actionsApiUrl', category=Optional[str])
    consumer_key = Field(default=random_string, null=True, json='consumerKey', category=Optional[str])
    secret_key = Field(default=random_string, null=True, json='secretKey', category=Optional[str])
    support_lti_review = Field(default=False, null=True, json='supportLtiReview', category=Optional[bool])
    support_lti_grading = Field(default=False, null=True, json='supportLtiGrading', category=Optional[bool])
    support_lti_authoring = Field(default=False, null=True, json='supportLtiAuthoring', category=Optional[bool])
    auth_url = Field(default=random_string, null=True, json='authUrl', category=Optional[str])


class ResourceLibrariesPublicFile(ResourceLibraries):
    extended_by = ResourceLibraries

    type = Field(default=SupportedResourceLibraryType.PUBLIC_FILE.value, json='type', category=int)
    bucket_name = Field(default=random_string, null=True, json='bucketName', category=Optional[str])
    subfolder = Field(default=random_string, null=True, json='subfolder', category=Optional[str])
    user = Field(default=random_string, null=True, json='user', category=Optional[str])
    password = Field(default=random_string, null=True, json='password', category=Optional[str])


class ResourceLibrariesPrivateFile(ResourceLibraries):
    extended_by = ResourceLibraries

    url = Field(default=f'https://{MINIO_HOST}', null=True, json='url', category=Optional[str])
    type = Field(default=SupportedResourceLibraryType.PRIVATE_FILE.value, json='type', category=int)
    bucket_name = Field(default=MINIO_PRIVATE_BUCKET_NAME, null=True, json='bucketName', category=Optional[str])
    subfolder = Field(default=None, null=True, json='subfolder', category=Optional[str])
    user = Field(default=MINIO_ACCESS_KEY, null=True, json='user', category=Optional[str])
    password = Field(default=MINIO_SECRET_KEY, null=True, json='password', category=Optional[str])
    allow_publishing = Field(default=True, json='allowPublishing', category=bool)
    allow_editing = Field(default=True, json='allowEditing', category=bool)


class ResourceLibrariesAction(Model):
    name = Field(default=None, json='name', category=Optional[str])
    url = Field(default=None, json='url', category=Optional[str])
    image_url = Field(default=None, null=True, json='imageUrl', category=Optional[str])


def get_default_resource_library():
    """Returns default resource library"""
    payload = ResourceLibrariesLTI13.manager.to_json
    return create_resource_library(payload).json()['id']


class CreateResourceLibraries(Model):
    database = USERS_DB_NAME
    identity = 'create_resource_library_id'

    create_resource_library_id = Field(category=str)


class UpdateResourceLibraries(Model):
    database = USERS_DB_NAME
    identity = 'update_resource_library_id'

    update_resource_library_id = Field(category=str)


class DeleteResourceLibraries(Model):
    database = USERS_DB_NAME
    identity = 'delete_resource_library_id'

    delete_resource_library_id = Field(category=str)


class SupportedResourceLibraryModel(Enum):
    """ Supported Types for Resource Libraries Model """
    LTI_1_3 = ResourceLibrariesLTI13, 'LTI 1.3'
    PUBLIC_FILE = ResourceLibrariesPublicFile, 'PublicFile'
    PRIVATE_FILE = ResourceLibrariesPrivateFile, 'PrivateFile'
    LTI_1_1 = ResourceLibrariesLTI11, 'LTI 1.1'

    @classmethod
    def to_list(cls) -> List[ResourceLibraries]:
        return [library_model.value[0] for library_model in cls]

    @classmethod
    def to_ids(cls):
        return [library_type.value[1] for library_type in cls]
