import uuid
from datetime import datetime
from typing import Optional

from models_manager import Field, Model

from models.utils.utils import get_email
from settings import DEFAULT_TENANT, USERS_DB_NAME
from utils.utils import random_string


class Users(Model):
    SCOPE = [
        {'name': 'User.Read', 'scope': 'Self', 'scopeType': 'User'},
        {'name': 'User.Read', 'scope': None, 'scopeType': None},
        {'name': 'User.Update', 'scope': None, 'scopeType': None},
        {'name': 'User.Delete', 'scope': None, 'scopeType': None},
        {'name': 'User.Create', 'scope': None, 'scopeType': None},
    ]
    database = USERS_DB_NAME
    identity = 'user_id'

    user_id = Field(default=uuid.uuid4, category=str, json='id')
    first_name = Field(default=random_string, json='firstName', max_length=200, category=str, null=True)
    last_name = Field(default=random_string, json='lastName', max_length=200, category=str)
    middle_name = Field(default=random_string, json='middleName', max_length=200, category=Optional[str], null=True)
    username = Field(default=random_string, json='username', max_length=200, category=str)
    email = Field(default=get_email, json='email', max_length=200, category=str)
    tenant_id = Field(default=DEFAULT_TENANT['id'], json='tenantId', is_related=True, category=str, optional=True)
    user_state = Field(default='2', category=str)
    roles_modified = Field(default=datetime.now, null=True, category=str)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    created_on_behalf_of_user_id = Field(default=uuid.uuid4, category=str)
    external_id = Field(default=random_string, json='externalId', category=Optional[str], null=True, max_length=200)

    def __str__(self):
        return f'<User {self.user_id}>'


def get_default_user():
    """Returns default user"""
    from base.api.users.users.users import create_user

    user_payload = Users.manager.to_json
    return create_user(user_payload).json()['id']


class CreateUsers(Model):
    database = USERS_DB_NAME
    identity = 'create_user_id'

    create_user_id = Field(category=str)


class UpdateUsers(Model):
    database = USERS_DB_NAME
    identity = 'update_user_id'

    update_user_id = Field(category=str)
