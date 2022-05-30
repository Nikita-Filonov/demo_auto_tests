from typing import Dict, Union

from pylenium.driver import Pylenium

from base.ui.learner.courses.courses import CoursesPage
from models.ztool.workflow import WorkflowDatetime
from utils.formatters.dates import DateTimeFormatters
from utils.ui.components.badge import Badge
from utils.ui.components.button import Button
from utils.ui.components.iframe import with_iframe, without_iframe
from utils.ui.components.item import Item
from utils.ui.components.modal import Modal
from utils.ui.components.textarea import Textarea


class CoursePage(CoursesPage):
    start_course_button = Button('//*[@data-qa="start-course-button"]', 'Start course')
    finish_course_button = Button('//*[@data-qa="finish-course-button"]', 'Finish course')
    exercise_textarea = Textarea('//*[@data-qa="exercise-textarea-{exercise_id}"]', 'Exercise textarea')
    answer_text = Item('//*[@data-qa="answer-text-{exercise_id}"]', 'Answer text')
    uploaded_file_button = Item('//button[@title="{file_name}"]', 'Uploaded file')
    submit_course_button = Button('//*[@data-qa="submit-course-button"]', 'Submit course')
    course_state_submitted_badge = Badge('//*[@data-qa="course-state-submitted-badge"]', 'Course submitted')
    course_state_in_grading_badge = Badge('//*[@data-qa="course-state-in-grading-badge"]', 'Course in grading')
    submission_confirm_modal = Modal('//*[@class="modal-new-body"]', 'Submission confirmation¬')
    submission_confirm_modal_cancel = Button('//*[@data-qa="submission-confirm-modal-cancel"]', 'Cancel')
    submission_confirm_modal_submit = Button('//*[@data-qa="submission-confirm-modal-submit"]', 'Submit')
    show_question_button = Button('//*[@data-qa="show-question-button"]', 'Show question')
    more_details_button = Button('//*[@data-qa="show-more-button"]', 'More details')

    def __init__(self, py: Pylenium, context: Dict[str, Union[dict, list]]):
        super().__init__(py, context)
        self.py = py
        self.context = context
        self.exercises = context['exercises']
        self.element = context['element']
        self.activity = context['activity']

    def click_start_course(self):
        self.start_course_button.click()
        self.start_course_button.disappear()

    def click_answer_next_button(self):
        self.answer_next_button.click()

    def fill_exercise_textarea(self, text, slug):
        exercise_id = self.get_exercise_id(slug)
        self.exercise_textarea.type(text, exercise_id=exercise_id)

    def exercise_textarea_visible(self, slug: str):
        exercise_id = self.get_exercise_id(slug)
        self.exercise_textarea.is_visible(exercise_id=exercise_id)

    def answer_contains_text(self, slug, text):
        exercise_id = self.get_exercise_id(slug)
        self.answer_text.contains_text(exercise_id=exercise_id, text=text)

    def answer_not_contains_text(self, slug, text):
        exercise_id = self.get_exercise_id(slug)
        self.answer_text.not_have_text(exercise_id=exercise_id, text=text)

    @with_iframe(CoursesPage.tool_iframe)
    def click_submit(self):
        self.submit_course_button.click()
        self.submission_confirm_modal.click()
        self.submission_confirm_modal_submit.click()

    @with_iframe(CoursesPage.tool_iframe)
    def course_state_submitted_badge_present(self):
        self.course_state_submitted_badge.is_visible()

    @with_iframe(CoursesPage.tool_iframe)
    def course_state_in_grading_badge_present(self):
        self.course_state_in_grading_badge.is_visible()

    @with_iframe(CoursesPage.tool_iframe)
    def is_submit_button_visible(self):
        self.submit_course_button.is_visible()

    def click_more_details(self):
        self.more_details_button.click()

    @without_iframe(CoursesPage.tool_iframe)
    def click_course_details_back(self):
        self.course_back_button.click()

    @with_iframe(CoursesPage.tool_iframe)
    def click_course_next(self):
        self.answer_next_button.click()

    @with_iframe(CoursesPage.tool_iframe)
    def submitted_datetime_is_in_correct_format(self):
        self.check_course_datetime(DateTimeFormatters.LEARNER_SUBMISSION_DATE_TIME_FORMAT, WorkflowDatetime.SUBMITTED)

    def finished_date_is_in_correct_format(self):
        self.check_course_datetime(DateTimeFormatters.COMMON_SHORT_DATE_FORMAT, WorkflowDatetime.FINISHED)

    def finished_date_is_in_correct_format_with_more_details(self):
        self.check_course_datetime(DateTimeFormatters.COMMON_SHORT_FULL_DATE_FORMAT, WorkflowDatetime.FINISHED)

    @with_iframe(CoursesPage.tool_iframe)
    def upload_file(self, file_path: str):
        super().upload_file(file_path)
