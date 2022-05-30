import uuid
from datetime import datetime

from models_manager import Field, Model

from base.api.users.group_users.group_users import create_group_user
from models.users.group import get_default_group
from settings import DEFAULT_TENANT, USERS_DB_NAME, DEFAULT_USER


class GroupUsers(Model):
    SCOPE = [
        {'name': 'GroupUser.Read', 'scope': None, 'scopeType': None},
        {'name': 'GroupUser.Create', 'scope': None, 'scopeType': None},
        {'name': 'GroupUser.Delete', 'scope': None, 'scopeType': None},
        {'name': 'GroupUser.Update', 'scope': None, 'scopeType': None},
    ]
    database = USERS_DB_NAME
    identity = 'group_user_id'

    group_user_id = Field(default=uuid.uuid4, json='id', category=str)
    tenant_id = Field(default=DEFAULT_TENANT['id'], is_related=True, category=str)
    user_id = Field(default=DEFAULT_USER['id'], json='userId', is_related=True, category=str, optional=True)
    group_id = Field(default=get_default_group, json='groupId', is_related=True, category=str, optional=True)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    created_on_behalf_of_user_id = Field(default=uuid.uuid4, category=str)

    def __str__(self):
        return f'<GroupUser {self.group_user_id}>'


def get_default_group_user():
    """Returns group user with default properties"""
    payload = GroupUsers.manager.to_json
    return create_group_user(payload).json()['id']


class CreateGroupUsers(Model):
    database = USERS_DB_NAME
    identity = 'create_group_user_id'

    create_group_user_id = Field(category=str)


class DeleteGroupUsers(Model):
    database = USERS_DB_NAME
    identity = 'delete_group_user_id'

    delete_group_user_id = Field(category=str)
