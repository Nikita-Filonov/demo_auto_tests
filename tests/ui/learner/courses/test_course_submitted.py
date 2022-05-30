import allure
import pytest

from base.ui.base_page import BaseUI
from parameters.courses.ui.ztool.answers import answers_null_properties
from parameters.courses.ui.ztool.attachments import answer_attachments_properties
from parameters.courses.ui.ztool.exercises import exercises_properties
from parameters.courses.ui.ztool.grades import grade_properties
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.learner import CoursesStory
from utils.api.utils import COMMON_FILES


@pytest.mark.ui
@pytest.mark.courses
@allure.epic('Core LMS')
@allure.feature('Learner (UI)')
@allure.tag('Smoke')
@allure.story(CoursesStory.COURSE_SUBMITTED.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestLearnerUiCourseSubmitted(BaseUI):
    exercise = exercises_properties[0]

    @allure.id("1364")
    @allure.title('Learner opens already submitted course (UI)')
    def test_learner_opens_already_submitted_course(self, course_page, submitted_workflow_ui):
        course_page.course_state_submitted_badge_present()

    @allure.id("4164")
    @allure.title('Learner clicks "Back" button (UI)')
    def test_learner_clicks_back_button_on_submitted_course_page(self, course_page, submitted_workflow_ui):
        course_page.click_course_back()
        course_page.is_courses_page_location()

    @allure.id("4163")
    @pytest.mark.parametrize('grade', grade_properties)
    def test_learner_checks_grades_on_submitted_course_page(self, course_page, submitted_workflow_ui, grade):
        allure.dynamic.title(f'Learner checks grades "{grade}" (UI)')
        course_page.grade_present(grade)

    @allure.id("4174")
    @allure.title('Learner can download Textbook attachment (UI)')
    def test_learner_downloads_textbook_attachment_on_submitted_course_page(self, course_page, submitted_workflow_ui):
        course_page.click_download_textbook_attachment()
        course_page.is_textbook_downloaded()

    @allure.id("4188")
    @pytest.mark.parametrize('file_path', COMMON_FILES)
    @pytest.mark.parametrize(
        'submitted_workflow_ui',
        [{'answers': answers_null_properties, 'answer_attachments': answer_attachments_properties}],
        indirect=['submitted_workflow_ui']
    )
    @allure.title(f'Learner downloads learner\'s attachment from the answer (UI)')
    def test_learner_downloads_learners_attachment_from_the_answer_on_submitted_course_page(self, course_page,
                                                                                            submitted_workflow_ui,
                                                                                            file_path):
        slug = self.exercise['slug']
        file_name = submitted_workflow_ui['answer_attachments'][0]['name']
        course_page.click_exercise(slug=slug)
        course_page.click_download_attachment(file_name)
        course_page.assert_downloaded_file(file_name)
