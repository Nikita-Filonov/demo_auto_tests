import allure
import pytest

from base.ui.base_page import BaseUI
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.learner import CoursesStory


@pytest.mark.ui
@pytest.mark.courses
@allure.epic('Core LMS')
@allure.feature('Learner (UI)')
@allure.tag('Smoke')
@allure.story(CoursesStory.COURSE_IN_GRADING.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestLearnerUiCourseInGrading(BaseUI):

    @allure.id("4410")
    @allure.title(f'Learner checks badge in grading state (UI)')
    def test_learner_opens_course_in_grading_state(self, in_grade_workflow_ui, course_page):
        course_page.course_state_in_grading_badge_present()
