import allure
import pytest

from base.ui.base_page import BaseTenantSettingsUI
from models.users.tenant_setting import SupportedSettings
from parameters.api.users.tenant_settings import custom_tenant_settings
from parameters.courses.ui.ztool.exercises import exercises_properties
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.administrator import AdministratorStory
from utils.api.users.tenant_settings import get_valid_file_size_alert_message, \
    get_extensions_from_mime_for_tenant_setting
from utils.api.utils import FILE_PATH
from utils.assertions.tenant_settings import assert_text_language_matches_language_setting


@pytest.mark.ui
@pytest.mark.tenant_settings_updates
@allure.epic('Core LMS')
@allure.feature('Administrator (UI)')
@allure.story(AdministratorStory.TENANT_SETTINGS.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestTenantSettingsUpdatesUi(BaseTenantSettingsUI):
    exercise_slug = exercises_properties[0]['slug']
    invalid_file = FILE_PATH + '/some.jpg'

    @allure.id("5315")
    @pytest.mark.parametrize(
        'update_tenant_setting_value',
        [{'key': SupportedSettings.LOCALE.value, 'value': custom_tenant_settings[SupportedSettings.LOCALE.value]}],
        indirect=['update_tenant_setting_value']
    )
    @allure.title('Admin update "Locale" tenant setting (UI)')
    def test_admin_update_locale_tenant_setting(self, update_tenant_setting_value, courses_page):
        text = courses_page.my_courses_title.get_text()
        assert_text_language_matches_language_setting(parsed_text=text)

    @allure.id("5316")
    @pytest.mark.parametrize(
        'update_tenant_setting_value',
        [{
            'key': SupportedSettings.STEM_UPLOAD_ATTACHMENT_SIZE_LIMIT.value,
            'value': custom_tenant_settings[SupportedSettings.STEM_UPLOAD_ATTACHMENT_SIZE_LIMIT.value]
        }],
        indirect=['update_tenant_setting_value']
    )
    @allure.title('Admin update "Attachment size limit" tenant setting (UI)')
    def test_admin_update_attachment_size_limit_tenant_setting(self, update_tenant_setting_value, course_page):
        course_page.click_exercise(slug=self.exercise_slug)
        course_page.upload_file(self.invalid_file)
        course_page.error_alert_message.contains_text(text=get_valid_file_size_alert_message())

    @allure.id("5318")
    @pytest.mark.parametrize(
        'update_tenant_setting_value',
        [{
            'key': SupportedSettings.STEM_UPLOAD_ACCEPTED_MIME_TYPES.value,
            'value': custom_tenant_settings[SupportedSettings.STEM_UPLOAD_ACCEPTED_MIME_TYPES.value]
        }],
        indirect=['update_tenant_setting_value']
    )
    @allure.title('Admin update "Accepted mime types" tenant setting (UI)')
    def test_admin_update_accepted_mime_types_tenant_setting(self, update_tenant_setting_value, course_page):
        course_page.click_exercise(slug=self.exercise_slug)
        course_page.upload_file(self.invalid_file)
        course_page.error_alert_message.contains_text(text=", ".join(get_extensions_from_mime_for_tenant_setting()))

    @allure.id("5317")
    @pytest.mark.parametrize(
        'update_tenant_setting_value',
        [{'key': SupportedSettings.HOME_URL.value, 'value': custom_tenant_settings[SupportedSettings.HOME_URL.value]}],
        indirect=['update_tenant_setting_value']
    )
    @pytest.mark.parametrize(
        'profile_page',
        [{'should_visit': False, 'should_login': False}],
        indirect=['profile_page']
    )
    @allure.title('Admin update "Home URL" tenant setting (UI)')
    def test_admin_update_home_url_tenant_setting(self, update_tenant_setting_value, courses_page, profile_page):
        courses_page.logo_button.click()
        profile_page.full_name_title.is_visible()
