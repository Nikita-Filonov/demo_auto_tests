import pytest
from alms_integration import create_oauth1_credentials

from base.api.users.datagrid_settings.datagrid_settings import create_data_grid_setting
from base.api.users.grading_scales.grading_scales import create_grading_scale
from base.api.users.lms_users.lms_users import create_lms_user
from base.api.users.permissions.permissions import create_permission
from base.api.users.resource_libraries.resource_libraries import create_resource_library
from base.api.users.role_pattern_permissions.role_pattern_permissions import create_role_pattern_permission
from base.api.users.roles.roles import create_role
from models.users.data_grid_settings import DataGridSettings
from models.users.grading_scale import GradingScales
from models.users.lms_user import LmsUsers
from models.users.mail_message import MailMessages
from models.users.oauth1_credentials import Oauth1Credentials
from models.users.permission import Permissions
from models.users.resource_libraries import ResourceLibrariesLTI11
from models.users.role import Roles
from models.users.role_pattern_permission import RolePatternPermissions
from parameters.api.users.resource_library import RESOURCE_LIBRARIES_VIRTUAL_LAB


@pytest.fixture(scope='function')
def lms_user():
    lms_user_payload = LmsUsers.manager.to_json
    return create_lms_user(lms_user_payload).json()


@pytest.fixture(scope='function')
def role():
    payload = Roles.manager.to_json
    return create_role(payload).json()


@pytest.fixture(scope='function')
def permission():
    permission_payload = Permissions.manager.to_json
    return create_permission(permission_payload).json()


@pytest.fixture(scope='function')
def role_pattern_permission(role_pattern):
    role_pattern_permission_payload = RolePatternPermissions.manager.to_json
    return create_role_pattern_permission(role_pattern_permission_payload).json()


@pytest.fixture(scope='function')
def oauth1_credentials():
    oauth1_credentials_payload = Oauth1Credentials.manager.to_json
    return create_oauth1_credentials(oauth1_credentials_payload).json()


@pytest.fixture(scope='function')
def data_grid_settings():
    data_grid_settings = DataGridSettings.manager.to_json
    return create_data_grid_setting(data_grid_settings).json()


@pytest.fixture(scope='function')
def mail_message(user_function):
    return MailMessages.manager.create(to_address=user_function['email'])


@pytest.fixture(scope='function')
def grading_scale():
    payload = GradingScales.manager.to_json
    return create_grading_scale(payload).json()


@pytest.fixture(scope='function')
def resource_library_virtual_lab():
    """
    Create resource library "Virtual Lab"
    """
    resource_library_payload = {**ResourceLibrariesLTI11.manager.to_json, **RESOURCE_LIBRARIES_VIRTUAL_LAB}
    return create_resource_library(resource_library_payload).json()
