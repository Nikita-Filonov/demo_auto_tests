from typing import List

from googletrans import Translator

from base.api.users.tenant_settings.tenant_settings import get_tenant_setting
from models.users.tenant_setting import SupportedSettings
from utils.utils import get_file_size, get_extensions_from_mime

translator = Translator()


def get_extensions_from_mime_for_tenant_setting() -> List[str]:
    """
    Used to get list of extensions for current tenant setting ``SupportedSettings.STEM_UPLOAD_ACCEPTED_MIME_TYPES``
    """
    mime_types_settings = get_tenant_setting(
        tenant_setting_id=SupportedSettings.STEM_UPLOAD_ACCEPTED_MIME_TYPES.value).json()
    return get_extensions_from_mime(mime_types_settings['value'], ignore_empty=True)


def get_valid_file_size_alert_message() -> str:
    """Get valid file size depended on tenant setting in format for Alert message"""
    size_file_limit_settings = get_tenant_setting(
        tenant_setting_id=SupportedSettings.STEM_UPLOAD_ATTACHMENT_SIZE_LIMIT.value).json()
    size_file_limit = int(size_file_limit_settings['value'])
    return get_file_size(size_file_limit)


def get_text_language(parsed_text: str) -> str:
    """Get text language 'en', 'ru' -> str"""
    return translator.detect(parsed_text).lang
