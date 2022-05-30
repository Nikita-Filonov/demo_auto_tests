import uuid
from datetime import datetime
from enum import Enum

from models_manager import Field, Model

from base.api.users.tenants.tenants import create_tenant
from models.users.user import Users
from settings import USERS_DB_NAME
from utils.utils import random_string


class SupportedTenants(Enum):
    ALEMIRA = 'Alemira'
    AUTOTEST = 'Autotest'
    OXFORD = 'Oxford'

    @classmethod
    def to_list(cls):
        return [tenant.value for tenant in cls]


def get_admin_user():
    return Users.manager.to_json


class Tenants(Model):
    SCOPE = [
        {'name': 'Tenant.Read', 'scope': None, 'scopeType': None},
        {'name': 'Tenant.Update', 'scope': None, 'scopeType': None},
        {'name': 'Tenant.Delete', 'scope': None, 'scopeType': None},
        {'name': 'Tenant.Create', 'scope': None, 'scopeType': None},
    ]
    database = USERS_DB_NAME
    identity = 'tenant_id'

    tenant_id = Field(default=uuid.uuid4, json='id', category=str)
    name = Field(default=random_string, json='name', category=str, max_length=200)
    admin_user = Field(
        default=get_admin_user,
        json='adminUser',
        category=dict,
        only_json=True,
        is_related=True,
        optional=True
    )
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    created_on_behalf_of_user_id = Field(default=uuid.uuid4, category=str)

    def __str__(self):
        return f'<Tenant {self.tenant_id}>'


def get_default_tenant():
    """Returns tenant with default properties"""
    payload = Tenants.manager.to_json
    return create_tenant(payload).json()['id']
