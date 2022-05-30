import allure
import pytest

from base.ui.base_page import BaseUI
from parameters.courses.ui.ztool.grades import grade_properties
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.learner import CoursesStory


@pytest.mark.ui
@pytest.mark.courses
@allure.epic('Core LMS')
@allure.feature('Learner (UI)')
@allure.story(CoursesStory.COURSE_FINISHED.value)
@allure.tag('Smoke')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestLearnerUiCourseGradedFinished(BaseUI):
    @allure.id("4089")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1423',
        name='Learner: missing back button on course details page (not started, finished)'
    )
    @allure.title('Learner clicks "Back" button (UI)')
    def test_learner_clicks_back_button_on_finished_course_page(self, finished_course_page):
        finished_course_page.click_course_details_back()
        finished_course_page.is_courses_page_location()

    @allure.id("4095")
    @allure.title('Learner can see the "Course name" (UI)')
    def test_learner_can_see_the_course_name_on_finished_course_page(self, finished_course_page):
        finished_course_page.text_present(finished_course_page.activity['name'])

    @allure.id("4092")
    @allure.title('Learner sees course\'s "Grade", "Score", "Date" results (UI)')
    def test_learner_sees_courses_grade_score_date_results_on_finished_course_page(self, finished_course_page):
        finished_course_page.click_more_details()
        finished_course_page.check_grade_and_score()
        finished_course_page.finished_date_is_in_correct_format()

    @allure.id("4090")
    @pytest.mark.parametrize('grade', grade_properties)
    def test_learner_checks_grades_on_finished_course_page(self, finished_course_page, grade):
        allure.dynamic.title(f'Learner checks grades "{grade}" with more details(UI)')
        finished_course_page.click_more_details()
        finished_course_page.grade_present(grade)

    @allure.id("4098")
    @allure.title('Learner unfolds and collapses textbook with more details (UI)')
    def test_learner_unfolds_and_collapses_textbook_on_finished_course_page(self, finished_course_page):
        finished_course_page.click_more_details()
        finished_course_page.toggle_textbook_collapse()
        finished_course_page.ui_course_link_is_visible()
        finished_course_page.toggle_textbook_collapse()
        finished_course_page.ui_course_link_disappear()

    @allure.id("4097")
    @allure.title('Learner downloads Textbook attachment with more details (UI)')
    def test_learner_downloads_textbook_attachment_on_finished_course_page(self, finished_course_page):
        finished_course_page.click_more_details()
        finished_course_page.click_download_textbook_attachment()
        finished_course_page.is_textbook_downloaded()

    @allure.id("4099")
    @allure.title('Learner sees course\'s "Grade", "Score", "Date" results with more details (UI)')
    def test_learner_sees_courses_grad_score_date_results_on_details_finished_course_page(self, finished_course_page):
        finished_course_page.click_more_details()
        finished_course_page.check_grade_and_score()
        finished_course_page.finished_date_is_in_correct_format_with_more_details()
