import allure
from assertions import assert_contains

from base.api.users.tenant_settings.tenant_settings import get_tenant_setting
from models.users.tenant_setting import SupportedSettings
from utils.api.users.tenant_settings import get_text_language


def assert_text_language_matches_language_setting(parsed_text: str):
    language_settings = get_tenant_setting(
        tenant_setting_id=SupportedSettings.LOCALE.value).json()
    language = get_text_language(parsed_text=parsed_text)
    with allure.step(f'Text "{parsed_text}" on page matches language setting "{language}"'):
        assert_contains(language, language_settings['value'],
                        what='Language on web page matches current custom language setting')
