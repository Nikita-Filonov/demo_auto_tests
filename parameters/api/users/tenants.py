import uuid

from base.api.users.tenants.tenants import get_tenants, get_tenant, create_tenant, update_tenant
from base.api.users.tenants.tenants_checks import is_tenant_created, is_tenant_updated
from models.users.tenant import Tenants

tenant_payload = Tenants
tenant_id = uuid.uuid4()

tenant_methods = [
    {'method': get_tenants, 'args': (), 'key': 'tenants.get_tenants'},
    {'method': get_tenant, 'args': (tenant_id,), 'key': 'tenants.get_tenant'},
    {'method': create_tenant, 'args': (tenant_payload,), 'key': 'tenants.create_tenant'},
    {'method': update_tenant, 'args': (tenant_id, tenant_payload,), 'key': 'tenants.update_tenant'},
    {'method': is_tenant_created, 'args': (tenant_id,), 'key': 'tenants.is_tenant_created'},
    {'method': is_tenant_updated, 'args': (tenant_id,), 'key': 'tenants.is_tenant_updated'},
]
