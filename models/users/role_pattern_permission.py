import uuid
from datetime import datetime
from typing import Optional

from models_manager import Field, Model

from base.api.users.role_pattern_permissions.role_pattern_permissions import create_role_pattern_permission
from models.users.role_pattern import get_default_role_pattern
from settings import DEFAULT_TENANT, USERS_DB_NAME
from utils.utils import random_string


class RolePatternPermissions(Model):
    SCOPE = [
        {'name': 'RolePatternPermission.Read', 'scope': None, 'scopeType': None},
        {'name': 'RolePatternPermission.Delete', 'scope': None, 'scopeType': None},
        {'name': 'RolePatternPermission.Update', 'scope': None, 'scopeType': None},
        {'name': 'RolePatternPermission.Create', 'scope': None, 'scopeType': None},
    ]
    database = USERS_DB_NAME
    identity = 'role_pattern_permission_id'

    role_pattern_permission_id = Field(default=uuid.uuid4, json='id', category=str)
    name = Field(
        default=random_string,
        json='name',
        category=Optional[str],
        max_length=200
    )
    scope = Field(
        default=random_string,
        json='scope',
        is_related=True,
        category=Optional[str],
        null=True,
        max_length=200
    )
    scope_type = Field(
        default=random_string,
        json='scopeType',
        category=Optional[str],
        null=True,
        max_length=50
    )
    tenant_id = Field(default=DEFAULT_TENANT['id'], is_related=True, category=str)
    role_pattern_id = Field(
        default=get_default_role_pattern,
        json='rolePatternId',
        is_related=True,
        category=str,
        optional=True
    )
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
        return f'<RolePatternPermission {self.role_pattern_id}, {self.name}>'


def get_default_role_pattern_permission():
    """Returns role pattern permission with default properties"""
    payload = RolePatternPermissions.manager.to_json
    return create_role_pattern_permission(payload).json()['id']


class CreateRolePatternPermissions(Model):
    database = USERS_DB_NAME
    identity = 'create_role_pattern_permission_id'

    create_role_pattern_permission_id = Field(category=str)


class DeleteRolePatternPermissions(Model):
    database = USERS_DB_NAME
    identity = 'delete_role_pattern_permission_id'

    delete_role_pattern_permission_id = Field(category=str)
