import os

import allure
import pytest

from base.ui.base_page import BaseUI
from parameters.courses.ui.ztool.answers import answers_null_properties
from parameters.courses.ui.ztool.attachments import answer_attachments_properties
from parameters.courses.ui.ztool.exercises import exercises_properties
from parameters.courses.ui.ztool.grades import grade_properties
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.learner import CoursesStory
from utils.api.utils import get_default_files, COMMON_FILES
from utils.utils import random_string


@pytest.mark.ui
@pytest.mark.courses
@allure.epic('Core LMS')
@allure.feature('Learner (UI)')
@allure.tag('Smoke')
@allure.story(CoursesStory.COURSE_IN_PROGRESS.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestLearnerUiCourseInProgress(BaseUI):
    exercise_1, exercise_2, question_1, question_2 = [exercise['slug'] for exercise in exercises_properties]
    EXCLUDE_FILES = ['some.json', 'some.txt']
    files = get_default_files(EXCLUDE_FILES)

    @allure.id("1363")
    @allure.title('Learner submits the course (UI)')
    def test_learner_submits_the_course(self, course_page):
        course_page.click_submit()
        course_page.course_state_submitted_badge_present()
        course_page.submitted_datetime_is_in_correct_format()

    @allure.id("3895")
    @allure.title('Learner clicks "Back" button (UI)')
    def test_learner_clicks_back_button_on_started_course_page(self, course_page):
        course_page.click_course_back()
        course_page.is_courses_page_location()

    @allure.id("3824")
    @pytest.mark.parametrize('text', [
        {'text': random_string(start=10, end=10)},
        {'text': random_string(start=2000, end=2000)}
    ], ids=['some_text', 'maximum_permissible_length_text'])
    def test_learner_enters_answer_with_permissible_text(self, request, course_page, text):
        allure.dynamic.title(f'Learner enters answer with permissible text "{request.node.callspec.id}" (UI)')
        course_page.click_exercise(slug=self.question_1)
        course_page.fill_exercise_textarea(text['text'], slug=self.question_1)
        course_page.click_exercise(slug=self.exercise_2)
        course_page.fill_exercise_textarea(text['text'], slug=self.exercise_2)
        course_page.answer_contains_text(slug=self.question_1, text=text['text'])
        course_page.click_exercise(slug=self.exercise_1)
        course_page.answer_contains_text(slug=self.exercise_2, text=text['text'])

    @allure.id("4063")
    @pytest.mark.parametrize('text', [
        {'text': random_string(start=2001, end=2001)}
    ], ids=['more_than_maximum_permissible_length_text'])
    def test_learner_enters_answer_with_impermissible_text(self, request, course_page, text):
        allure.dynamic.title(f'Learner enters answer with impermissible text "{request.node.callspec.id}" (UI)')
        course_page.click_exercise(slug=self.question_1)
        course_page.fill_exercise_textarea(text['text'], slug=self.question_1)
        course_page.click_exercise(slug=self.exercise_2)
        course_page.fill_exercise_textarea(text['text'], slug=self.exercise_2)
        course_page.answer_not_contains_text(slug=self.question_1, text=text)
        course_page.click_exercise(slug=self.exercise_1)
        course_page.answer_not_contains_text(slug=self.exercise_2, text=text)

    @allure.id("4096")
    @pytest.mark.parametrize('text', [
        {'text': random_string(start=10, end=10)}
    ], ids=['text'])
    @allure.title('Answer data saving after 3 seconds (UI)')
    def test_answers_data_saving_on_started_course_page(self, course_page, text):
        course_page.click_exercise(slug=self.exercise_1)
        course_page.fill_exercise_textarea(text['text'], slug=self.exercise_1)

        course_page.wait_until_answer_is_saved()
        course_page.answer_contains_text(slug=self.exercise_1, text=text['text'])

    @allure.id("3825")
    @pytest.mark.parametrize('file_path', files)
    def test_learner_uploads_attachment_to_the_answer(self, course_page, file_path):
        allure.dynamic.title(f'Learner uploads attachment "{os.path.basename(file_path)}" to the answer (UI)')
        course_page.click_exercise(slug=self.exercise_1)
        course_page.upload_file(file_path)
        course_page.is_file_present(file_path)

    @allure.id("3867")
    @pytest.mark.parametrize('file_path', COMMON_FILES)
    @pytest.mark.parametrize(
        'started_course_ui',
        [{'answers': answers_null_properties, 'answer_attachments': answer_attachments_properties}],
        indirect=['started_course_ui']
    )
    @allure.title(f'Learner removes learner\'s attachment from the answer (UI)')
    def test_learner_removes_learners_attachment_from_the_answer(self, course_page, started_course_ui, file_path):
        file_name = started_course_ui['answer_attachments'][0]['name']
        course_page.click_exercise(slug=self.exercise_1)
        course_page.click_remove_answer_file(file_name)
        course_page.text_not_present(file_name)

    @allure.id("4052")
    @allure.title('Learner downloads Textbook attachment (UI)')
    def test_learner_downloads_textbook_attachment_on_started_course_page(self, course_page):
        course_page.click_download_textbook_attachment()
        course_page.is_textbook_downloaded()

    @allure.id("4161")
    @pytest.mark.parametrize('grade', grade_properties)
    def test_learner_checks_grades_on_started_course_page(self, course_page, grade):
        allure.dynamic.title(f'Learner checks grades "{grade}" (UI)')
        course_page.grade_present(grade)

    @allure.id("4162")
    @allure.title('Learner clicks "Next" button (UI)')
    def test_learner_clicks_next_button_on_started_course_page(self, course_page):
        course_page.click_exercise(slug=self.question_1)
        course_page.click_course_next()
        course_page.exercise_textarea_visible(slug=self.question_2)

    @allure.id("4165")
    @pytest.mark.parametrize('file_path', COMMON_FILES)
    @pytest.mark.parametrize(
        'started_course_ui',
        [{'answers': answers_null_properties, 'answer_attachments': answer_attachments_properties}],
        indirect=['started_course_ui']
    )
    @allure.title(f'Learner downloads learner\'s attachment from the answer (UI)')
    def test_learner_downloads_learners_attachment_from_the_answer_on_started_course_page(self, course_page,
                                                                                          started_course_ui,
                                                                                          file_path):
        file_name = started_course_ui['answer_attachments'][0]['name']
        course_page.click_exercise(slug=self.exercise_1)
        course_page.click_download_attachment(file_name)
        course_page.assert_downloaded_file(file_name)
