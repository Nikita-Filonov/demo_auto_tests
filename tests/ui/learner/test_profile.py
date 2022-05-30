import allure
import pytest

from base.ui.base_page import BaseUI
from settings import RERUNS, RERUNS_DELAY, DEFAULT_USER
from utils.allure.stories.ui.learner import LearnerProfile


@pytest.mark.ui
@pytest.mark.learner_profile
@allure.epic('Core LMS')
@allure.feature('Learner')
@allure.story(LearnerProfile.LEARNER_PROFILE.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestProfileUI(BaseUI):
    @allure.id("4225")
    @allure.title('Learner clicks "Back" button (UI)')
    def test_learner_clicks_back_button_on_profile_page(self, profile_page):
        profile_page.click_profile_back()
        profile_page.is_courses_page_location()

    @allure.id("4218")
    @allure.title('Learner checks user info (UI)')
    def test_learner_checks_user_info_on_profile_page(self, profile_page):
        profile_page.first_name.have_value(DEFAULT_USER["first_name"])
        profile_page.last_name.have_value(DEFAULT_USER["last_name"])
        profile_page.username.have_value(DEFAULT_USER["username"])
        profile_page.email.have_value(DEFAULT_USER["username"])

    @allure.id("4217")
    @allure.title('Learner checks course\'s results table (UI)')
    def test_learner_courses_results_table_on_profile_page(self, profile_page_with_course):
        profile_page_with_course.check_grade_and_score_on_profile_page()
        profile_page_with_course.row_course_name_contains_course_name()
        profile_page_with_course.row_course_date_is_in_correct_format()
