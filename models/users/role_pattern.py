import uuid
from datetime import datetime
from enum import Enum
from typing import List, Dict

from models_manager import Field, Model

from settings import DEFAULT_TENANT, USERS_DB_NAME
from utils.utils import random_string


class SupportedRolePatterns(Enum):
    GROUP_OWNER = 'GroupOwner_{0}'
    GROUP_INSTRUCTOR = 'GroupInstructor_{0}'

    @staticmethod
    def normalize_group_id(group_id: str) -> str:
        """
        Used to normalize group_id for scope

        Example:
            some_id = '43ec0584-9570-484b-a74c-78f2b10a5a00'
            SupportedRolePatterns.normalize_group_id(some_id) -> '43ec05849570484ba74c78f2b10a5a00'
        """
        return group_id.replace('-', '')

    @classmethod
    def get_owner_role(cls, group_id: str) -> str:
        safe_group_id = cls.normalize_group_id(group_id)
        return cls.GROUP_OWNER.value.format(safe_group_id)

    @classmethod
    def get_instructor_role(cls, group_id: str) -> str:
        safe_group_id = cls.normalize_group_id(group_id)
        return cls.GROUP_INSTRUCTOR.value.format(safe_group_id)

    @classmethod
    def to_list(cls, group_id: str) -> List[Dict[str, str]]:
        """
        Used to convert join group roles with group id

        Example:
            some_id = '43ec0584-9570-484b-a74c-78f2b10a5a00'
            SupportedRolePatterns.to_list(some_id) ->
            [
                {'name': 'GroupOwner_43ec05849570484ba74c78f2b10a5a00'},
                {'name': 'GroupInstructor_43ec05849570484ba74c78f2b10a5a00'}
            ]
        """
        safe_group_id = cls.normalize_group_id(group_id)
        return [{'name': role.value.format(safe_group_id)} for role in SupportedRolePatterns]

    @classmethod
    def to_group_owner_scope(cls, group_id: str) -> List[Dict[str, str]]:
        from models.utils.users.role_patterns import GROUP_OWNER_SCOPE, ROLE_PATTERN_SCOPE_TYPE
        safe_group_id = cls.normalize_group_id(group_id)
        return [
            {**scope, 'scope': safe_group_id, 'scopeType': ROLE_PATTERN_SCOPE_TYPE}
            for scope in GROUP_OWNER_SCOPE
        ]

    @classmethod
    def to_group_instructor_scope(cls, group_id: str) -> List[Dict[str, str]]:
        from models.utils.users.role_patterns import GROUP_INSTRUCTOR_SCOPE, ROLE_PATTERN_SCOPE_TYPE
        safe_group_id = cls.normalize_group_id(group_id)
        return [
            {**scope, 'scope': safe_group_id, 'scopeType': ROLE_PATTERN_SCOPE_TYPE}
            for scope in GROUP_INSTRUCTOR_SCOPE
        ]


class RolePatterns(Model):
    SCOPE = [
        {'name': 'RolePattern.Read', 'scope': None, 'scopeType': None},
        {'name': 'RolePattern.Delete', 'scope': None, 'scopeType': None},
        {'name': 'RolePattern.Update', 'scope': None, 'scopeType': None},
        {'name': 'RolePattern.Create', 'scope': None, 'scopeType': None},
    ]
    database = USERS_DB_NAME
    identity = 'role_pattern_id'

    role_pattern_id = Field(default=uuid.uuid4, json='id', category=str)
    name = Field(default=random_string, json='name', category=str)
    scope_type = Field(default=random_string, json='scopeType', category=str)
    tenant_id = Field(default=DEFAULT_TENANT['id'], is_related=True, category=str)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    created_on_behalf_of_user_id = Field(default=uuid.uuid4, category=str)
    modified = Field(default=None, null=True, category=str)
    modified_by_user_id = Field(default=None, null=True, category=str)
    modified_on_behalf_of_user_id = Field(default=None, null=True, category=str)

    def __str__(self):
        return f'<RolePattern {self.role_pattern_id}, {self.name}>'


def get_default_role_pattern():
    """Returns default role pattern with default properties"""
    return RolePatterns.manager.create(as_json=False).role_pattern_id.value


class CreateRolePatterns(Model):
    database = USERS_DB_NAME
    identity = 'create_role_pattern_id'

    create_role_pattern_id = Field(category=str)


class UpdateRolePatterns(Model):
    database = USERS_DB_NAME
    identity = 'update_role_pattern_id'

    update_role_pattern_id = Field(category=str)


class DeleteRolePatterns(Model):
    database = USERS_DB_NAME
    identity = 'delete_role_pattern_id'

    delete_role_pattern_id = Field(category=str)
