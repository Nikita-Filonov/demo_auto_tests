import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

from models_manager import Field, Model

from settings import DEFAULT_TENANT, USERS_DB_NAME
from utils.utils import random_string


class SupportedRoles(Enum):
    LEARNER = 'Learner'
    AUTHOR = 'Author'
    INSTRUCTOR = 'Instructor'
    OBSERVER = 'Observer'
    ADMINISTRATOR = 'Administrator'
    TENANT_ADMIN = 'TenantAdmin'

    @classmethod
    def to_list(cls, exclude: Optional[List['SupportedRoles']] = None):
        safe_exclude = exclude or []
        return [role.value for role in cls if role not in safe_exclude]


class Roles(Model):
    ROLES = [
        SupportedRoles.INSTRUCTOR.value,
        SupportedRoles.LEARNER.value,
        SupportedRoles.AUTHOR.value,
        SupportedRoles.ADMINISTRATOR.value
    ]
    SCOPE = [
        {'name': 'Role.Read', 'scope': None, 'scopeType': None},
        {'name': 'Role.Delete', 'scope': None, 'scopeType': None},
        {'name': 'Role.Update', 'scope': None, 'scopeType': None},
        {'name': 'Role.Create', 'scope': None, 'scopeType': None},
    ]
    database = USERS_DB_NAME
    identity = 'role_id'

    role_id = Field(default=uuid.uuid4, json='id', category=str)
    tenant_id = Field(default=DEFAULT_TENANT['id'], json='tenantId', is_related=True, category=str, optional=True)
    name = Field(default=random_string, json='name', category=str, max_length=200)
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
        return f'<Role {self.role_id}, {self.name}>'


def get_default_role():
    """Returns role with default properties"""
    from base.api.users.roles.roles import create_role
    payload = Roles.manager.to_json
    return create_role(payload).json()['id']


class RolePermissions(Model):
    database = USERS_DB_NAME
    identity = 'RolesId'

    role_id = Field(default=None, category=str)
    permission_id = Field(default=None, json='id', category=str)
    name = Field(json='name', category=str, only_json=True)
    application_id = Field(json='applicationId', category=str, only_json=True)
    scope = Field(json='scope', category=Optional[str], only_json=True, null=True)
    scope_type = Field(json='scopeType', category=Optional[str], only_json=True, null=True)
    tenant = Field(json='tenant', category=dict, only_json=True)
    roles = Field(json='roles', category=list, only_json=True)


class CreateRoles(Model):
    database = USERS_DB_NAME
    identity = 'create_role_id'

    create_role_id = Field(category=str)


class UpdateRoles(Model):
    database = USERS_DB_NAME
    identity = 'update_role_id'

    update_role_id = Field(category=str)


class DeleteRoles(Model):
    database = USERS_DB_NAME
    identity = 'delete_role_id'

    delete_role_id = Field(category=str)
