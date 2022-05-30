import uuid
from datetime import datetime
from typing import Optional

from models_manager import Field, Model

from base.api.users.permissions.permissions import create_permission
from settings import DEFAULT_TENANT, USERS_DB_NAME
from utils.utils import random_string


class Permissions(Model):
    SCOPE = [
        {'name': 'Permission.Read', 'scope': None, 'scopeType': None},
        {'name': 'Permission.Delete', 'scope': None, 'scopeType': None},
        {'name': 'Permission.Update', 'scope': None, 'scopeType': None},
        {'name': 'Permission.Create', 'scope': None, 'scopeType': None},
    ]
    database = USERS_DB_NAME
    identity = 'permission_id'

    permission_id = Field(default=uuid.uuid4, json='id', category=str)
    tenant_id = Field(default=DEFAULT_TENANT['id'], json='tenantId', is_related=True, category=str, optional=True)
    name = Field(default=random_string, json='name', category=str, max_length=200)
    application_id = Field(default=uuid.uuid4, json='applicationId', category=str)
    scope = Field(default=random_string, json='scope', null=True, category=Optional[str], max_length=200)
    scope_type = Field(default=random_string, json='scopeType', null=True, category=Optional[str], max_length=50)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    created_on_behalf_of_user_id = Field(default=uuid.uuid4, category=str)
    modified = Field(default=None, null=True, category=str)
    modified_by_user_id = Field(default=None, null=True, category=str)
    modified_on_behalf_of_user_id = Field(default=None, null=True, category=str)
    removed = Field(default=None, null=True, category=str)
    removed_by_user_id = Field(default=None, null=True, category=str)
    removed_on_behalf_of_user_id = Field(default=None, null=True, category=str)

    def __str__(self):
        return f'<Permission {self.permission_id}, {self.name}>'


def get_default_permission():
    """Returns permission with default properties"""
    payload = Permissions.manager.to_json
    return create_permission(payload).json()['id']
