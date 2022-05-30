from enum import Enum


class AdministratorStory(Enum):
    USERS = 'Users'
    GROUPS = 'Groups'
    OBJECTIVES = 'Objectives'
    ROLE_PATTERNS = 'Role patterns'
    TENANTS = 'Tenants'
    RESOURCE_LIBRARY = 'Resource library'
    TENANT_SETTINGS = 'Tenant Settings'
