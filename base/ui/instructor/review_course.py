from typing import Dict, Union

import allure
from pylenium.driver import Pylenium

from base.ui.author.author_page import AuthorPage
from models.ztool.answer import Answers
from models.ztool.element import Elements
from models.ztool.exercise import Exercises
from models.ztool.workflow import WorkflowStates, WorkflowDatetime
from models.ztool.workflow import Workflows
from utils.formatters.dates import DateTimeFormatters
from utils.ui.components.button import Button
from utils.ui.components.collapse import Collapse
from utils.ui.components.input import Input
from utils.ui.components.modal import Modal
from utils.ui.components.textarea import Textarea
from utils.ui.utils import get_grade_class


class ReviewCoursePage(AuthorPage):
    feedback_textarea = Textarea('//*[@data-qa="feedback-textarea"]', 'Feedback')
    bonus_score_input = Input('//*[@data-qa="bonus-score-input"]', 'Bonus score', Elements.max_bonus.default)
    penalty_score_input = Input('//*[@data-qa="penalty-score-input"]', 'Penalty score', Elements.max_bonus.default)

    approve_button = Button(f'//*[@data-qa="submit-workflow-{WorkflowStates.GRADED.value}-button"]', 'Approve')
    send_for_approval_button = Button(
        f'//*[@data-qa="submit-workflow-{WorkflowStates.IN_GRADING.value}-button"]',
        text='Send for approval'
    )
    grade_is_published_badge = '//*[@data-qa="grade-is-published-badge"]'
    grade_is_approved_badge = '//*[@data-qa="grade-is-approved-badge"]'
    general_feedback_label = '//*[@data-qa="general-feedback-label"]'
    no_answer_message_label = '//*[@data-qa="no-answer-message-label"]'
    exercise_grade_input = Input('//*[@data-qa="exercise-grade-{exercise_id}-input"]', 'Exercise grade')
    exercise_feedback_textarea = Textarea(
        '//*[@data-qa="exercise-feedback-{exercise_id}-textarea"]',
        label='Exercise feedback'
    )
    answer_score_text_label = '//*[@data-qa="{exercise_id}-{grade_class}-label"]'
    exercise_unfold_toggle = Collapse('//*[@data-qa="exercise-{exercise_id}-unfold-toggle"]', 'Exercise unfold')
    exercise_collapse_toggle = Collapse('//*[@data-qa="exercise-{exercise_id}-collapse-toggle"]', 'Exercise collapse')
    feedback_input_file = Input('//*[@data-qa="feedback-input-file-{answer_id}"]', 'Feedback')
    show_tutor_guide_popup_button = Button(
        '//*[@data-qa="show-tutor-guide-popup-{exercise_id}-button"]',
        text='Show tutor guide popup'
    )
    approve_modal = Modal('//*[@class="modal-new-body"]', 'Approve modal')

    def __init__(self, py: Pylenium, context: Dict[str, Union[dict, list]]):
        super().__init__(py, context)
        self.py = py
        self.context = context
        self.element = context['element']

        self.tool_iframe.switch_to_iframe()

    def click_send_for_approval(self):
        self.send_for_approval_button.click()
        self.approve_modal.is_visible()
        self.click_confirm_modal_yes_button()

    def click_approve(self):
        self.approve_button.is_clickable()
        self.approve_button.click()

        self.approve_modal.click()
        self.click_confirm_modal_yes_button()

    def fill_answer_score(self, score: int, slug):
        exercise_id = self.get_exercise_id(slug)
        self.exercise_grade_input.type(score, exercise_id=exercise_id)

    def fill_answer_feedback(self, feedback: str, slug):
        exercise_id = self.get_exercise_id(slug)
        self.exercise_feedback_textarea.type(feedback, exercise_id=exercise_id)

    def check_score_label(self, score, slug):
        """Used to check score label and color"""
        exercise = Exercises.manager.get(element_id=self.element['element_id'], slug=slug)
        grade_class = get_grade_class(exercise['max_score'], score)

        score_label_locator = self.answer_score_text_label.format(exercise_id=exercise['exercise_id'],
                                                                  grade_class=grade_class)
        score_label_text = f'{score}/{int(exercise["max_score"])}'

        self.element_should_have_text(score_label_locator, score_label_text)

    def check_penalty_score(self):
        """Used to check penalty score value depends on result score"""
        result_score = self.get_grade_and_score_result_value()['score']
        self.penalty_score_input.have_value(value=result_score)

    def answer_score_should_have_value(self, score, slug):
        exercise_id = self.get_exercise_id(slug)
        self.exercise_grade_input.have_value(score, exercise_id=exercise_id)

    def answer_feedback_should_have_value(self, feedback, slug):
        exercise_id = self.get_exercise_id(slug)
        self.exercise_feedback_textarea.have_value(feedback, exercise_id=exercise_id)

    @allure.step('Checking that workflow was sent for approval')
    def is_sent_for_approval(self):
        self.wait_for_expected_state(self.learner['workflow_id'], WorkflowStates.GRADED)
        self.approve_button.is_visible()

    def submitted_date_is_in_correct_format(self):
        self.check_course_datetime(DateTimeFormatters.INSTRUCTOR_DATE_TIME_FORMAT, WorkflowDatetime.SUBMITTED)

    def graded_date_is_in_correct_format(self):
        self.check_course_datetime(DateTimeFormatters.INSTRUCTOR_DATE_TIME_FORMAT, WorkflowDatetime.GRADED)

    def approved_date_is_in_correct_format(self):
        self.check_course_datetime(DateTimeFormatters.INSTRUCTOR_DATE_TIME_FORMAT, WorkflowDatetime.GRADE_APPROVED)

    @allure.step('Checking that workflow was approved')
    def is_approved(self):
        self.element_present(self.grade_is_approved_badge, 'Grade is approved badge')
        self.element_present(self.general_feedback_label, 'General feedback label')

        workflow = Workflows.manager.get(workflow_id=self.learner['workflow_id'])

        self.text_present(workflow['feedback'])
        self.bonus_score_input.is_readonly()
        self.penalty_score_input.is_readonly()

    @allure.step('Checking that "No answer message" present on the page')
    def no_answer_message_label_resent(self):
        self.element_present(self.no_answer_message_label, 'No answer message')

    def toggle_exercise_unfold(self, slug):
        exercise_id = self.get_exercise_id(slug)

        self.exercise_unfold_toggle.click(exercise_id=exercise_id)
        self.exercise_collapse_toggle.is_visible(exercise_id=exercise_id)

    def toggle_exercise_collapse(self, slug):
        exercise_id = self.get_exercise_id(slug)

        self.exercise_collapse_toggle.click(exercise_id=exercise_id)
        self.exercise_unfold_toggle.is_visible(exercise_id=exercise_id)

    def upload_file_to_answer(self, slug: str, file_path: str):
        exercise_id = self.get_exercise_id(slug)
        answer = Answers.manager.get(workflow_id=self.learner['workflow_id'], exercise_id=exercise_id)
        self.feedback_input_file.attach_file(file_path, answer_id=answer['answer_id'])

    def click_show_tutor_guide_popup(self, slug):
        exercise_id = self.get_exercise_id(slug)
        self.show_tutor_guide_popup_button.click(exercise_id=exercise_id)

    def check_tutor_guideline(self, slug):
        exercise_id = self.get_exercise_id(slug)
        exercise = Exercises.manager.get(exercise_id=exercise_id)
        self.text_present(exercise['tutor_guideline'])
        self.text_present(exercise['correct_answer'])

    def exercise_grade_input_not_visible(self, slug):
        with allure.step('Input area for grading should not be visible'):
            exercise_id = self.get_exercise_id(slug)
            self.exercise_grade_input.disappear(exercise_id=exercise_id)
