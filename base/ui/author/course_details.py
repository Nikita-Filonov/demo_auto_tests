from typing import Dict, Any, Union

from pylenium.driver import Pylenium

from base.ui.author.author_page import AuthorPage
from models.utils.utils import get_min_bonus
from models.ztool.element import Grades, Elements
from models.ztool.exercise import Exercises
from models.ztool.workflow import WorkflowStates
from settings import DEBUG
from utils.ui.components.button import Button
from utils.ui.components.collapse import Collapse
from utils.ui.components.form import Form
from utils.ui.components.icon import Icon
from utils.ui.components.input import Input
from utils.ui.components.item import Item
from utils.ui.components.link import Link
from utils.ui.components.tab import Tab
from utils.ui.components.text import Text
from utils.ui.components.textarea import Textarea
from utils.utils import random_string, random_number


class CourseDetailsPage(AuthorPage):
    textbook_textarea = Textarea('//*[@data-qa="textbook-textarea"]', 'Textbook', Elements.textbook.get_default)
    tutor_guidelines_textarea = Textarea('//*[@data-qa="tutor-guidelines-textarea"]', 'Tutor guidelines', random_string)
    min_instructor_bonus_input = Input(
        '//*[@data-qa="min-instructor-bonus-input"]',
        'Min instructor bonus',
        get_min_bonus
    )
    max_instructor_bonus_input = Input(
        '//*[@data-qa="max-instructor-bonus-input"]',
        'Max instructor bonus',
        random_number
    )
    start_of_grading_date_input = Input('//*[@data-qa="start-of-grading-date-input"]', 'Start of grading date')
    end_of_grading_date_input = Input('//*[@data-qa="end-of-grading-date-input"]', 'End of grading date')
    grading_disclosure_date_input = Input(
        '//*[@data-qa="grading-disclosure-date-input"]',
        label='Grading disclosure date'
    )
    course_form = Form([
        textbook_textarea, tutor_guidelines_textarea,
        min_instructor_bonus_input, max_instructor_bonus_input
    ])
    update_course_button = Button('//*[@data-qa="update-course-button"]', 'Update course')
    preview_course_button = Button('//*[@data-qa="preview-course-button"]', 'Preview course')
    go_to_course_edit_button = Button('//*[@data-qa="go-to-course-edit-button"]', 'Go to edit course')
    exercise_link = Link('//*[@data-qa="exercise-link-{exercise_id}"]', 'Exercise link')
    exercise_title = Text('//*[@data-qa="exercise-title-{exercise_id}"]', 'Exercise title')
    send_all_submitted_courses_to_grading_link = Link(
        '//*[@data-qa="send-all-submitted-courses-to-grading-link"]',
        text='Send all submitted courses to grading'
    )
    send_all_grading_approved_courses_to_finished_link = Link(
        '//*[@data-qa="send-all-grading-approved-to-finished-link"]',
        text='Send all grading approved courses to finished'
    )
    grade_input = Input('//*[@data-qa="grade-{grade_id}-input"]', 'Grade')
    files_tab = Tab('//*[@data-qa="files-tab"]', 'Files tab')
    dates_tab = Tab('//*[@data-qa="dates-tab"]', 'Dates tab')
    editor_tab = Tab('//*[@data-qa="editor-tab"]', 'Editor tab')
    file_row = Item('//*[@data-qa="file-row-{file_name}"]', 'File row')
    delete_file_button = Button('//*[@data-qa="{file_name}-delete-file-button"]', 'Delete file')
    copy_file_button = Button('//*[@data-qa="{file_name}-copy-file-link-button"]', 'Copy file')
    link_copied_icon = Icon('//*[@data-qa="{file_name}-link-copied-icon"]', 'File copied icon')
    exercise_group_collapse = Collapse('//*[@data-qa="exercise-group-{group}-collapse"]', 'Exercise group')

    def __init__(self, py: Pylenium, context: Dict[str, Union[dict, list]]):
        super().__init__(py, context)
        self.py = py
        self.context = context
        self.element = context['element']

    def click_update_course(self):
        self.update_course_button.click()

    def click_exercise_group_collapse(self, group: str):
        self.exercise_group_collapse.click(group=group)

    def click_exercise_link(self, slug: str):
        exercise_id = Exercises.manager.get(slug=slug, element_id=self.element['element_id'])['exercise_id']
        self.exercise_title.hover(exercise_id=exercise_id)
        self.exercise_link.click(exercise_id=exercise_id)

    def get_grade_id(self, name: str):
        return Grades.manager.get(element_id=self.element['element_id'], name=name)['grade_id']

    def click_send_all_grading_approved_courses_to_finished_link(self, expected_state: WorkflowStates):
        self.send_all_grading_approved_courses_to_finished_link.click()
        self.wait_for_expected_state(self.context[self.roles.LEARNER]['workflow_id'], expected_state)

    def click_send_all_submitted_courses_to_grading_link(self, expected_state: WorkflowStates):
        self.send_all_submitted_courses_to_grading_link.click()
        self.wait_for_expected_state(self.context[self.roles.LEARNER]['workflow_id'], expected_state)

    def grade_input_value_equals(self, name: str, value: Any):
        grade_id = self.get_grade_id(name)
        self.grade_input.have_value(value, grade_id=grade_id)

    def fill_grade(self, name: str, value: Any):
        grade_id = self.get_grade_id(name)
        self.grade_input.type(value, grade_id=grade_id)

    def clear_grade_input(self, name):
        grade_id = self.get_grade_id(name)
        self.grade_input.clear(grade_id=grade_id)

    def click_remove_file(self, file_name: str):
        self.file_row.hover(file_name=file_name)
        self.delete_file_button.click(file_name=file_name)

    def click_copy_file(self, file_name: str):
        self.file_row.hover(file_name=file_name)
        self.copy_file_button.click(file_name=file_name)

    def file_link_copied(self, file_name):
        """
        Ensure that file link was copied to clipboard or that
        error with file link is present.

        In standalone, we have a limitation on coping to clipboard
        """
        if DEBUG:
            self.link_copied_icon.is_visible(file_name=file_name)
        else:
            self.error_alert_present()
