import os

import allure
import pytest

from base.ui.instructor.review_course import ReviewCoursePage
from parameters.courses.ui.ztool.answers import answers_null_properties
from parameters.courses.ui.ztool.attachments import answer_attachments_properties, feedback_attachments_properties
from parameters.courses.ui.ztool.exercises import exercises_properties
from parameters.courses.ui.ztool.grades import grade_properties
from settings import RERUNS, RERUNS_DELAY
from tests.api.ztool.conftest import EXCLUDE_FILES
from utils.api.utils import get_default_files, COMMON_FILES
from utils.utils import random_string


@pytest.mark.ui
@pytest.mark.instructor_review_course
@allure.epic('Core LMS')
@allure.feature('Instructor and Observer (UI)')
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestReviewCourseUi:
    exercise = exercises_properties[0]
    files = get_default_files(EXCLUDE_FILES)

    @allure.id("4039")
    @pytest.mark.parametrize('grade', grade_properties)
    def test_instructor_checks_grades(self, in_grade_review_course_page, grade):
        allure.dynamic.title(f'Instructor checks grades "{grade}" (UI)')
        in_grade_review_course_page.grade_present(grade)

    @allure.id("4043")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1351',
        name='Refactor test 4043 penalty score'
    )
    @allure.title('Send course for approval with penalty score(UI)')
    def test_send_course_for_approval_with_penalty_score(self, in_grade_review_course_page):
        text = random_string()
        in_grade_review_course_page.penalty_score_input.type()
        in_grade_review_course_page.feedback_textarea.type(value=text)
        in_grade_review_course_page.click_send_for_approval()
        in_grade_review_course_page.is_sent_for_approval()
        in_grade_review_course_page.check_grade_and_score()
        in_grade_review_course_page.check_penalty_score()
        in_grade_review_course_page.feedback_textarea.have_value(value=text)
        in_grade_review_course_page.submitted_date_is_in_correct_format()

    @allure.id("5049")
    @allure.title('Send course for approval with bonus score(UI)')
    def test_send_course_for_approval_with_bonus_score(self, in_grade_review_course_page):
        text = random_string()
        in_grade_review_course_page.bonus_score_input.type()
        in_grade_review_course_page.feedback_textarea.type(value=text)
        in_grade_review_course_page.click_send_for_approval()
        in_grade_review_course_page.is_sent_for_approval()
        in_grade_review_course_page.check_grade_and_score()
        in_grade_review_course_page.bonus_score_input.have_value(
            value=in_grade_review_course_page.bonus_score_input.value
        )
        in_grade_review_course_page.feedback_textarea.have_value(value=text)
        in_grade_review_course_page.submitted_date_is_in_correct_format()

    @allure.id("4046")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-969',
        name='/api/v1/objectives/{id}/objective-workflow-aggregate returns 204 status code'
    )
    @allure.title('Approve course (UI)')
    @pytest.mark.parametrize('score_adding', (
            ReviewCoursePage.bonus_score_input,
            ReviewCoursePage.penalty_score_input
    ))
    def test_approve_course(self, graded_review_course_page, score_adding):
        text = random_string()
        score_adding.clear()
        score_adding.type()
        graded_review_course_page.feedback_textarea.type(value=text)
        graded_review_course_page.click_approve()
        graded_review_course_page.is_approved()
        graded_review_course_page.check_grade_and_score()
        score_adding.have_value(value=score_adding.value)
        graded_review_course_page.approved_date_is_in_correct_format()

    @allure.id("4186")
    @allure.title('Instructor sees "No answer" message if there is no answer from learner (UI)')
    def test_instructor_sees_no_answer_message(self, in_grade_review_course_page):
        in_grade_review_course_page.click_exercise(self.exercise['slug'])
        in_grade_review_course_page.no_answer_message_label_resent()

    @allure.id("4045")
    @allure.title('Instructor unfolds and collapses textbook (UI)')
    def test_instructor_unfolds_and_collapses_textbook(self, in_grade_review_course_page):
        in_grade_review_course_page.toggle_textbook_collapse()
        in_grade_review_course_page.ui_course_link_is_visible()
        in_grade_review_course_page.toggle_textbook_collapse()
        in_grade_review_course_page.ui_course_link_disappear()

    @allure.id("4042")
    @allure.title('Instructor downloads Textbook attachment (UI)')
    def test_instructor_downloads_textbook_attachment(self, in_grade_review_course_page):
        in_grade_review_course_page.click_download_textbook_attachment()
        in_grade_review_course_page.is_textbook_downloaded()

    @allure.id("4041")
    @pytest.mark.parametrize('score', [
        {'score': score, 'feedback': random_string()}
        for score in range(exercise['max_score'] + 1)
    ])
    @pytest.mark.parametrize(
        'submitted_workflow_ui',
        [{'answers': answers_null_properties}],
        indirect=['submitted_workflow_ui']
    )
    def test_instructor_enters_a_grade_for_students_answers(self, in_grade_review_course_page, submitted_workflow_ui,
                                                            score):
        allure.dynamic.title(f'Instructor enters a grade for student\'s answers with score "{score["score"]}" (UI)')
        slug = self.exercise['slug']
        in_grade_review_course_page.click_exercise(slug=slug)
        in_grade_review_course_page.fill_answer_score(score['score'], slug=slug)
        in_grade_review_course_page.fill_answer_feedback(score['feedback'], slug=slug)
        in_grade_review_course_page.wait_until_answer_is_saved()
        in_grade_review_course_page.check_score_label(score['score'], slug=slug)
        in_grade_review_course_page.click_exercise(slug=slug)
        in_grade_review_course_page.answer_score_should_have_value(score['score'], slug=slug)
        in_grade_review_course_page.answer_feedback_should_have_value(score['feedback'], slug=slug)

    @allure.id("4049")
    @allure.title('Instructor unfolds and collapses the question (UI)')
    def test_instructor_unfolds_and_collapses_the_question(self, in_grade_review_course_page):
        slug = self.exercise['slug']
        in_grade_review_course_page.click_exercise(slug=slug)
        in_grade_review_course_page.toggle_exercise_unfold(slug=slug)
        in_grade_review_course_page.toggle_exercise_collapse(slug=slug)

    @allure.id("4036")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-859',
        name='Observer: For grading: Observer can not attach a file'
    )
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-969',
        name='/api/v1/objectives/{id}/objective-workflow-aggregate returns 204 status code'
    )
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1267',
        name='Add tenant settings for autotests tenant'
    )
    @pytest.mark.parametrize('file_path', files)
    @pytest.mark.parametrize(
        'submitted_workflow_ui',
        [{'answers': answers_null_properties}],
        indirect=['submitted_workflow_ui']
    )
    def test_instructor_uploads_attachment_to_the_answer(self, in_grade_review_course_page, submitted_workflow_ui,
                                                         file_path):
        allure.dynamic.title(f'Instructor uploads attachment "{os.path.basename(file_path)}" to the answer (UI)')
        slug = self.exercise['slug']
        in_grade_review_course_page.click_exercise(slug=slug)
        in_grade_review_course_page.upload_file_to_answer(slug=slug, file_path=file_path)
        in_grade_review_course_page.is_file_present(file_path)

    @allure.id("4054")
    @allure.title('Instructor checks learner\'s attachment to the answer (UI)')
    @pytest.mark.parametrize('file_path', COMMON_FILES)
    @pytest.mark.parametrize(
        'submitted_workflow_ui',
        [{'answers': answers_null_properties, 'answer_attachments': answer_attachments_properties}],
        indirect=['submitted_workflow_ui']
    )
    def test_instructor_checks_learners_attachment_to_the_answer(self, in_grade_review_course_page,
                                                                 submitted_workflow_ui, file_path):
        slug = self.exercise['slug']
        in_grade_review_course_page.click_exercise(slug=slug)
        in_grade_review_course_page.is_file_present(submitted_workflow_ui['answer_attachments'][0]['name'])

    @allure.id("4056")
    @allure.title('Instructor removes instructor\'s attachment from the answer(UI)')
    @pytest.mark.parametrize('file_path', COMMON_FILES)
    @pytest.mark.parametrize(
        'submitted_workflow_ui',
        [{'answers': answers_null_properties, 'feedback_attachments': feedback_attachments_properties}],
        indirect=['submitted_workflow_ui']
    )
    def test_instructor_removes_instructors_attachment_from_the_answer(self, in_grade_review_course_page,
                                                                       submitted_workflow_ui, file_path):
        slug = self.exercise['slug']
        file_name = submitted_workflow_ui['feedback_attachments'][0]['name']
        in_grade_review_course_page.click_exercise(slug=slug)
        in_grade_review_course_page.click_remove_answer_file(file_name)
        in_grade_review_course_page.text_not_present(file_name)

    @allure.id("4057")
    @allure.title('Instructor can not send result form to approval without filling (UI)')
    def test_instructor_can_not_send_result_form_to_approval_without_filling(self, in_grade_review_course_page):
        in_grade_review_course_page.send_for_approval_button.is_disabled()

    @allure.id("4053")
    @allure.title('Instructor clicks "Back" button (UI)')
    @pytest.mark.parametrize(
        'for_grading_page',
        [{'should_visit': False, 'should_login': False}],
        indirect=['for_grading_page']
    )
    def test_instructor_clicks_back_button(self, in_grade_review_course_page, for_grading_page):
        in_grade_review_course_page.click_course_back()
        for_grading_page.for_grading_title_should_be_visible()

    @allure.id("4055")
    @allure.title('Instructor checks tutor guideline (UI)')
    def test_instructor_checks_tutor_guideline(self, in_grade_review_course_page):
        slug = self.exercise['slug']
        in_grade_review_course_page.click_exercise(slug=slug)
        in_grade_review_course_page.click_show_tutor_guide_popup(slug)
        in_grade_review_course_page.check_tutor_guideline(slug)

    @allure.id("4044")
    @allure.title('Instructor can not enter a grade without learner\'s answer (UI)')
    def test_instructor_can_not_enter_a_grade_without_learners_answer(self, in_grade_review_course_page):
        slug = self.exercise['slug']
        in_grade_review_course_page.click_exercise(slug=slug)
        in_grade_review_course_page.exercise_grade_input_not_visible(slug=slug)
