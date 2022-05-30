from typing import Union

from models.users.tenant import Tenants
from settings import DEFAULT_USER


def get_safe_tenants(extra_users: Union[list, tuple] = None, extra_tenants: Union[list, tuple] = None) -> tuple:
    """
    :param extra_users: list or tuple of users ids to exclude
    :param extra_tenants: list or tuple of tenants ids to exclude
    :return: tuple of tenants ids that can be deleted/modified
    """
    tenants = Tenants.manager.filter(created_by_user_id__in=(DEFAULT_USER['id'], *(extra_users or [])))
    return *tuple(tenant['tenant_id'] for tenant in tenants), *(extra_tenants or [])
