from typing import List, Dict

from models.identity.asp_net_user import AspNetUsers
from models.utils.users.roles import create_role
from settings import DEFAULT_USER
from utils.utils import random_string


def user_with_permissions(scopes: List[Dict], user: dict) -> dict:
    """
    :param scopes: scopes of permissions. For example
    [
        {'name': 'Activity.Read', 'scope': None, 'scopeType': None},
        {'name': 'Activity.Delete', 'scope': None, 'scopeType': None},
        {'name': 'Activity.Update', 'scope': None, 'scopeType': None},
        {'name': 'Activity.Create', 'scope': None, 'scopeType': None},
    ]
    :param user: user to give permissions
    :return: Created user, with permissions

    Used to create user with given ``scopes`` of permission
    """
    role_payload = {
        'name': random_string(),
        'scopes': scopes,
        'user_id': user['id']
    }
    create_role(**role_payload)
    return {
        **DEFAULT_USER,
        'password': AspNetUsers.Password.value,
        'username': user['email'],
        'scopes': scopes
    }
