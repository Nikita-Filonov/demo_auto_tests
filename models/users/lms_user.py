import uuid
from datetime import datetime
from typing import Optional

from models_manager import Field, Model

from models.users.user import Users
from settings import DEFAULT_TENANT, USERS_DB_NAME
from utils.utils import random_dict


class LmsUsers(Users):
    extended_by = Users

    details = Field(default=random_dict, null=False, category=dict, json='details')

    def __str__(self):
        return f'<LmsUser {self.user_id}>'


class UserExtensions(Model):
    database = USERS_DB_NAME
    identity = 'user_extension_id'

    user_extension_id = Field(default=uuid.uuid4, category=str, json='id')
    tenant_id = Field(default=DEFAULT_TENANT['id'], json='tenantId', is_related=True, category=str, optional=True)
    data = Field(default=random_dict, null=False, json='data', category=Optional[dict])
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
        return f'<UserExtension {self.user_extension_id}>'
