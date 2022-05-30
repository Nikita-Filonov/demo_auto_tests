import allure
import pytest

from base.ui.base_page import BaseUI
from models.users.objective import Objectives
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.learner import CoursesStory


@pytest.mark.ui
@pytest.mark.courses
@allure.epic('Core LMS')
@allure.feature('Learner (UI)')
@allure.tag('Smoke')
@allure.story(CoursesStory.COURSE_NOT_STARTED.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestLearnerUiCourseNotStarted(BaseUI):
    @allure.id("1361")
    @allure.title('Learner can not see the course without access (UI)')
    def test_learner_can_not_see_the_course_without_access(self, courses_page, objective_function):
        courses_page.text_not_present(objective_function[Objectives.name.json])

    @allure.id("1362")
    @allure.title('Learner clicks the course card (UI)')
    def test_learner_clicks_the_course_card(self, courses_page):
        courses_page.click_course_card()
        courses_page.course_title_present()

    @allure.id("3873")
    @allure.title('Learner clicks "Start the course" button (UI)')
    def test_learner_clicks_start_course_button(self, course_details_page):
        course_details_page.click_start_course()
        course_details_page.is_submit_button_visible()
        course_details_page.text_present('Autotests Course')

    @allure.id("3894")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1423',
        name='Learner: missing back button on course details page (not started, finished)'
    )
    @allure.title('Learner clicks "Back" button on course details page (UI)')
    def test_learner_clicks_back_button_on_course_detail_page(self, course_details_page):
        course_details_page.click_course_details_back()
        course_details_page.is_courses_page_location()
