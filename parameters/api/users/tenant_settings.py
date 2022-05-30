import json
import uuid

from base.api.users.tenant_settings.tenant_settings import get_tenant_settings, get_tenant_setting, \
    create_tenant_setting, update_tenant_setting, delete_tenant_setting, get_tenant_settings_query
from base.api.users.tenant_settings.tenant_settings_checks import is_tenant_setting_created, is_tenant_setting_updated, \
    is_tenant_setting_deleted
from models.users.tenant_setting import SupportedSettings, TenantSettings
from utils.ui.constants import SupportedLanguages

tenant_setting_id = uuid.uuid4()
tenant_setting_payload = TenantSettings

tenant_settings_methods = [
    {
        'method': get_tenant_settings,
        'args': (),
        'key': 'tenant_settings.get_tenant_settings'
    },
    {
        'method': get_tenant_setting,
        'args': (tenant_setting_id,),
        'key': 'tenant_settings.get_tenant_setting'
    },
    {
        'method': create_tenant_setting,
        'args': (tenant_setting_payload,),
        'key': 'tenant_settings.create_tenant_setting'
    },
    {
        'method': update_tenant_setting,
        'args': (tenant_setting_id, tenant_setting_payload),
        'key': 'tenant_settings.update_tenant_setting'
    },
    {
        'method': delete_tenant_setting,
        'args': (tenant_setting_id,),
        'key': 'tenant_settings.delete_tenant_setting'
    },
    {
        'method': is_tenant_setting_created,
        'args': (tenant_setting_id,),
        'key': 'tenant_settings.is_tenant_setting_created'
    },
    {
        'method': is_tenant_setting_updated,
        'args': (tenant_setting_id,),
        'key': 'tenant_settings.is_tenant_setting_updated'
    },
    {
        'method': is_tenant_setting_deleted,
        'args': (tenant_setting_id,),
        'key': 'tenant_settings.is_tenant_setting_deleted'
    },
    {
        'method': get_tenant_settings_query,
        'args': ('?skip=0&take=10&requireTotalCount=true',),
        'key': 'tenant_settings.get_tenant_settings_query'
    }
]

FILE_STORAGE_CONFIG = {
    "PublicBucket": "minio_public_bucket_name",
    "PrivateBucket": "minio_private_bucket_name",
    "AccessKey": "minio_access_key",
    "SecretKey": "minio_secret_key",
    "Host": "https://host.docker.internal:9000",
    "LinkLifetime": "00:01:00",
    "SignatureVersion": "4",
    "UseChunkEncoding": True,
    "ForcePathStyle": True,
    "SignatureMethod": 1,
    "AuthenticationRegion": "auto",
    "S3SupportPolicy": True,
    "S3SupportACL": False
}

UPLOAD_ACCEPTED_MIME_TYPES = [
    'image/tiff',
    'image/jpeg',
    'image/png',
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.oasis.opendocument.text'
    'application/vnd.oasis.opendocument.spreadsheet',
    'application/vnd.oasis.opendocument.presentation'
]

MAIL_SENDER = {
    "from_address": "Python Pytest <pytest2@example.com>",
    "use_ssl": False,
    "host": "host.docker.internal",
    "port": 1025
}

MAX_FILE_SIZE_LIMIT = '10485760'

default_tenant_settings = [
    (SupportedSettings.LOCALE.value, SupportedLanguages.EN.value),
    (SupportedSettings.LOGO.value, 'logo'),
    (
        SupportedSettings.FILE_STORAGE_CONFIG.value,
        json.dumps(FILE_STORAGE_CONFIG, skipkeys=True, separators=(',', ':'))
    ),
    (SupportedSettings.HOME_URL.value, ''),
    (SupportedSettings.STEM_UPLOAD_ACCEPTED_MIME_TYPES.value, ','.join(UPLOAD_ACCEPTED_MIME_TYPES)),
    (SupportedSettings.STEM_UPLOAD_ATTACHMENT_SIZE_LIMIT.value, MAX_FILE_SIZE_LIMIT),
    (SupportedSettings.PLATFORM_UPLOAD_ACCEPTED_MIME_TYPES.value, ','.join(UPLOAD_ACCEPTED_MIME_TYPES)),
    (SupportedSettings.PLATFORM_UPLOAD_ATTACHMENT_SIZE_LIMIT.value, MAX_FILE_SIZE_LIMIT),
    (
        SupportedSettings.MAIL_SENDER.value,
        json.dumps(MAIL_SENDER, skipkeys=True, separators=(',', ':'))
    )
]

custom_tenant_settings = {
    SupportedSettings.LOCALE.value: SupportedLanguages.RU.value,
    SupportedSettings.LOGO.value: 'logoZFTSH',
    SupportedSettings.HOME_URL.value: 'profile',
    SupportedSettings.STEM_UPLOAD_ACCEPTED_MIME_TYPES.value: 'image/png,application/msword',
    SupportedSettings.STEM_UPLOAD_ATTACHMENT_SIZE_LIMIT.value: '30000',
}
