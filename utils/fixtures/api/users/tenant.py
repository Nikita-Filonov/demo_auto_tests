import pytest

from base.api.users.tenants.tenants import create_tenant
from models.users.tenant import Tenants


@pytest.fixture(scope='function')
def tenant_function():
    payload = Tenants.manager.to_json
    return create_tenant(payload).json()


@pytest.fixture(scope='class')
def tenant_class():
    payload = Tenants.manager.to_json
    return create_tenant(payload).json()
