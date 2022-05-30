import uuid
from datetime import datetime

from models_manager import Field, Model

from base.api.users.groups.groups import create_group
from settings import DEFAULT_TENANT, USERS_DB_NAME
from utils.utils import random_string


class Groups(Model):
    SCOPE = [
        {'name': 'Group.Read', 'scope': None, 'scopeType': None},
        {'name': 'Group.Delete', 'scope': None, 'scopeType': None},
        {'name': 'Group.Update', 'scope': None, 'scopeType': None},
        {'name': 'Group.Create', 'scope': None, 'scopeType': None},
    ]
    database = USERS_DB_NAME
    identity = 'group_id'

    group_id = Field(default=uuid.uuid4, json='id', category=str)
    name = Field(default=random_string, json='name', category=str, max_length=400)
    tenant_id = Field(default=DEFAULT_TENANT['id'], is_related=True, category=str)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    created_on_behalf_of_user_id = Field(default=uuid.uuid4, category=str)
    modified = Field(default=None, null=True, category=str)
    modified_by_user_id = Field(default=None, null=True, category=str)
    modified_on_behalf_of_user_id = Field(default=None, null=True, category=str)

    def __str__(self):
        return f'<Group {self.group_id}, {self.name}>'


def get_default_group():
    """Returns default group"""
    payload = Groups.manager.to_json
    return create_group(payload).json()['id']


class CreateGroups(Model):
    database = USERS_DB_NAME
    identity = 'create_group_id'

    create_group_id = Field(category=str)


class UpdateGroups(Model):
    database = USERS_DB_NAME
    identity = 'update_group_id'

    update_group_id = Field(category=str)


class DeleteGroups(Model):
    database = USERS_DB_NAME
    identity = 'delete_group_id'

    delete_group_id = Field(category=str)
