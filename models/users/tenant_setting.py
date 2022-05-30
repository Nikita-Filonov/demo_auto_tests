import uuid
from datetime import datetime

from models_manager import Field, Model, FieldGenericEnum

from base.api.users.tenant_settings.tenant_settings import create_tenant_setting
from settings import USERS_DB_NAME, DEFAULT_TENANT
from utils.utils import random_string


class SupportedSettings(FieldGenericEnum):
    LOCALE = 'platform.common.locale'
    LOGO = 'platform.common.logo'
    FILE_STORAGE_CONFIG = 'platform.common.file_storage_config'
    HOME_URL = 'platform.common.home_url'
    STEM_UPLOAD_ACCEPTED_MIME_TYPES = 'stem.common.upload_accepted_mime_types'
    STEM_UPLOAD_ATTACHMENT_SIZE_LIMIT = 'stem.common.upload_attachment_size_limit'
    PLATFORM_UPLOAD_ATTACHMENT_SIZE_LIMIT = 'platform.file_resources.upload_attachment_size_limit'
    PLATFORM_UPLOAD_ACCEPTED_MIME_TYPES = 'platform.file_resources.upload_accepted_mime_types'
    MAIL_SENDER = 'mailsender.settings'


class TenantSettings(Model):
    SCOPE = [
        {'name': 'TenantSetting.Read', 'scope': None, 'scopeType': None},
        {'name': 'TenantSetting.Update', 'scope': None, 'scopeType': None},
        {'name': 'TenantSetting.Delete', 'scope': None, 'scopeType': None},
        {'name': 'TenantSetting.Create', 'scope': None, 'scopeType': None},
    ]
    database = USERS_DB_NAME
    identity = 'tenant_setting_id'

    tenant_setting_id = Field(default=uuid.uuid4, json='id', category=str)
    tenant_id = Field(default=DEFAULT_TENANT['id'], category=str)
    application_id = Field(default=uuid.uuid4, category=str)
    name = Field(default=random_string, json='name', category=str, max_length=400)
    value = Field(default=random_string, json='value', category=str)
    can_remove = Field(default=True, json='canRemove', category=bool)
    can_edit = Field(default=True, json='canEdit', category=bool)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    created_on_behalf_of_user_id = Field(default=uuid.uuid4, category=str)
    modified_by_user_id = Field(default=None, null=True, category=str)
    modified_on_behalf_of_user_id = Field(default=None, null=True, category=str)

    def __str__(self):
        return f'<TenantSetting {self.tenant_setting_id}>'


def get_default_tenant_setting():
    """Returns tenant setting with default properties"""
    payload = TenantSettings.manager.to_json
    return create_tenant_setting(payload).json()['id']
