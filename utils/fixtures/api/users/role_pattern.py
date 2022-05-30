import pytest

from base.api.users.role_patterns.role_patterns import create_role_pattern
from models.users.role_pattern import RolePatterns


@pytest.fixture(scope='function')
def role_pattern():
    role_pattern_payload = RolePatterns.manager.to_json
    return create_role_pattern(role_pattern_payload).json()
