import uuid
from datetime import datetime

from models_manager import Field, Model

from base.api.users.user_roles.user_roles import create_user_role
from models.users.role import get_default_role
from settings import DEFAULT_TENANT, USERS_DB_NAME, DEFAULT_USER


class CreateUserRole(Model):
    role_id = Field(json='roleId', category=str)
    user_id = Field(json='userId', category=str)


class UserRoles(Model):
    SCOPE = [
        {'name': 'UserRole.Read', 'scope': None, 'scopeType': None},
        {'name': 'UserRole.Delete', 'scope': None, 'scopeType': None},
        {'name': 'UserRole.Create', 'scope': None, 'scopeType': None},
        {'name': 'UserRole.Update', 'scope': None, 'scopeType': None},
    ]
    database = USERS_DB_NAME
    identity = 'user_role_id'

    user_role_id = Field(default=uuid.uuid4, json='id', category=str)
    tenant_id = Field(default=DEFAULT_TENANT['id'], json='tenantId', is_related=True, category=str)
    user_id = Field(default=DEFAULT_USER['id'], json='userId', category=str, optional=True)
    role_id = Field(default=get_default_role, json='roleId', is_related=True, category=str, optional=True)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    created_on_behalf_of_user_id = Field(default=uuid.uuid4, category=str)

    def __str__(self):
        return f'<UserRole {self.user_role_id}>'


def get_default_user_role():
    """Returns user role with default properties"""
    payload = UserRoles.manager.to_json
    return create_user_role(payload).json()['id']


class CreateUserRoles(Model):
    database = USERS_DB_NAME
    identity = 'create_user_role_id'

    create_user_role_id = Field(category=str)


class DeleteUserRoles(Model):
    database = USERS_DB_NAME
    identity = 'delete_user_role_id'

    delete_user_role_id = Field(category=str)
