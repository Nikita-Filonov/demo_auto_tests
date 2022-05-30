import uuid

from base.api.users.role_patterns.role_patterns import get_role_pattern, get_role_patterns, create_role_pattern, \
    delete_role_pattern, update_role_pattern, get_role_patterns_query
from base.api.users.role_patterns.role_patterns_checks import is_role_patterns_created, is_role_patterns_deleted, \
    is_role_patterns_updated
from models.users.role_pattern import RolePatterns

role_pattern_id = uuid.uuid4()
role_pattern_payload = RolePatterns

role_pattern_methods = [
    {'method': get_role_patterns, 'args': (), 'key': 'role_patterns.get_role_patterns'},
    {'method': get_role_pattern, 'args': (role_pattern_id,), 'key': 'role_patterns.get_role_pattern'},
    {'method': create_role_pattern, 'args': (role_pattern_payload,), 'key': 'role_patterns.create_role_pattern'},
    {'method': delete_role_pattern, 'args': (role_pattern_id,), 'key': 'role_patterns.delete_role_pattern'},
    {'method': update_role_pattern, 'args': (role_pattern_id, role_pattern_payload),
     'key': 'role_patterns.update_role_pattern'},
    {'method': is_role_patterns_created, 'args': (role_pattern_id,), 'key': 'role_patterns.is_role_patterns_created'},
    {'method': is_role_patterns_deleted, 'args': (role_pattern_id,), 'key': 'role_patterns.is_role_patterns_deleted'},
    {'method': is_role_patterns_updated, 'args': (role_pattern_id,), 'key': 'role_patterns.is_role_patterns_updated'},
    {'method': get_role_patterns_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
     'key': 'role_patterns.get_role_patterns_query'}
]
