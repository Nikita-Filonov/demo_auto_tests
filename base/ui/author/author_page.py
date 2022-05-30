from typing import Dict, Union

import allure

from base.ui.base_page import BasePage
from models.users.role import SupportedRoles
from models.ztool.answer import Answers
from models.ztool.attachment import ElementTextbookAttachments
from models.ztool.element import Grades
from models.ztool.exercise import Exercises
from models.ztool.workflow import Workflows, WorkflowStates, WorkflowDatetime
from utils.api.utils import parse_filename_from_url
from utils.formatters.dates import DateTimeFormatters
from utils.ui.components.button import Button
from utils.ui.components.collapse import Collapse
from utils.ui.components.iframe import with_iframe
from utils.ui.components.item import Item
from utils.ui.components.link import Link
from utils.ui.components.row import Row
from utils.ui.utils import normalized_grades, datetime_format
from utils.utils import file_name_or_path_resolve
from utils.utils import wait


class AuthorPage(BasePage):
    COURSE_TITLE = 'UI Course'
    download_textbook_attachment_button = Button(
        '//*[@data-qa="download-textbook-attachment-button"]',
        'Download textbook attachment'
    )
    remove_answer_file_button = Button('//*[@data-qa="remove-answer-file-{file_name}"]', 'Remove answer file')
    course_back_button = Button('//*[@data-qa="course-back-button"]', 'Back')
    answer_file_button = Button('//*[@data-qa="answer-file-{file_name}-button"]', 'Answer file')
    grade_estimation_title = Row('//*[@data-qa="grade-estimation-title"]', 'Grade estimation')
    total_score_title = Row('//*[@data-qa="total-score-title"]', 'Total score')
    row_score = Row('//*[@data-qa="row-score-{grade_id}"]', 'Score')
    row_grade = Row('//*[@data-qa="row-grade-{grade_id}"]', 'Grade')
    course_textbook_collapse = Collapse('//*[@data-qa="course-textbook-collapse"]', 'Course textbook')
    exercise_item = Item('//*[@data-qa="exercise-{exercise_id}"]', 'Exercise')
    answer_next_button = Button('//*[@data-qa="answer-next-button"]', 'Next')
    ui_course_link = Link('//*[@data-qa="ui-course-link"]', COURSE_TITLE)

    WAIT_UNTIL_ANSWER_IS_SAVED = 3
    roles = SupportedRoles

    def __init__(self, py, context: Dict[Union[str, SupportedRoles], Union[dict, list]]):
        super().__init__(py)

        self.context = context
        self.element = context['element']
        self.grades = context['grades']
        self.learner = context.get(self.roles.LEARNER, {})
        self.exercises = context['exercises']
        self.objective = context['objective']

    @staticmethod
    def wait_for_expected_state(workflow_id, expected_state: WorkflowStates):
        with allure.step(f'Waiting until workflow state will become {expected_state.value}'):
            wait(
                lambda: Workflows.manager.get(workflow_id=workflow_id)['state'] == expected_state.value,
                waiting_for=f'Waiting until workflow state equal to "{expected_state.value}"'
            )

    @allure.step('Checking that textbook was successfully downloaded')
    def is_textbook_downloaded(self):
        textbook_url = ElementTextbookAttachments.manager.get(element_id=self.element['element_id'])['url']
        file_name = parse_filename_from_url(textbook_url)
        self.assert_downloaded_file(file_name)

    @allure.step('Waiting until answer is saved')
    def wait_until_answer_is_saved(self):
        self.wait_for(self.WAIT_UNTIL_ANSWER_IS_SAVED, 'until answer is saved')
        self.reload()
        self.tool_iframe.switch_to_iframe()

    @allure.step('Checking that file present on the page')
    def is_file_present(self, file_path_or_name: str):
        safe_file_name = file_name_or_path_resolve(file_path_or_name)
        self.answer_file_button.is_visible(file_name=safe_file_name)

    def get_exercise_id(self, slug):
        """Should be used to get ``exercise_id`` by ``slug``"""
        return Exercises.manager.get(element_id=self.element['element_id'], slug=slug)['exercise_id']

    @with_iframe(BasePage.tool_iframe)
    def click_download_textbook_attachment(self):
        self.download_textbook_attachment_button.click()

    def click_remove_answer_file(self, file_path_or_name: str):
        safe_file_name = file_name_or_path_resolve(file_path_or_name)
        self.remove_answer_file_button.click(file_name=safe_file_name)

    @with_iframe(BasePage.tool_iframe)
    def click_course_back(self):
        self.course_back_button.click()

    @with_iframe(BasePage.tool_iframe)
    def grade_present(self, grade: Dict[str, Union[str, int]]):
        """
        Checking that grade row is present. Grade row might look like
        | score | grade |
        | 0 - 8 |   2   |
        """
        grade_id = Grades.manager.get(element_id=self.element['element_id'], **grade)['grade_id']
        normalized_grade = list(filter(lambda g: g['grade_id'] == grade_id, normalized_grades(self.grades)))[0]
        score_text = f'{int(normalized_grade["min"])} – {int(normalized_grade["max"])}'

        self.row_grade.is_visible(grade['name'], grade_id=grade_id)
        self.row_score.is_visible(score_text, grade_id=grade_id)

    def get_grade_and_score_result_value(self):
        """Should be used to check ``Total grade`` and ``Correspondent score``"""
        workflow = Workflows.manager.get(workflow_id=self.learner['workflow_id'])  # current workflow
        answers = Answers.manager.filter(workflow_id=self.learner['workflow_id'])  # all answers for that workflow

        # max score is based on all available scores that student can get. To calculate
        # the maximum score we have to map through the all exercises and sum their max score
        max_score = int(sum([exercise['max_score'] for exercise in self.exercises]))

        # score is based on total answers scores, so we have to map thought the all answers
        # and sum their scores. After that we have to add bonus score too
        score = int(sum([answer['score'] for answer in answers])) + int(workflow['bonus'])
        safe_score = max_score if score > max_score else (0 if score < 0 else score)

        correspondent_score = f'{safe_score}/{max_score}'
        total_grade = next(filter(lambda g: g['max'] >= safe_score, self.grades))['name']
        return {'score': safe_score, 'correspondent_score': correspondent_score, 'total_grade': total_grade}

    @with_iframe(BasePage.tool_iframe)
    @allure.step('Checking that grade and score are correct')
    def check_grade_and_score(self):
        grade_and_score_result = self.get_grade_and_score_result_value()

        self.grade_estimation_title.is_visible(grade_and_score_result['total_grade'])
        self.total_score_title.is_visible(grade_and_score_result['correspondent_score'])

    @with_iframe(BasePage.tool_iframe)
    def toggle_textbook_collapse(self):
        self.course_textbook_collapse.click()

    @with_iframe(BasePage.tool_iframe)
    def click_exercise(self, slug):
        """"
        Do click on question or exercise to show answer text area

        :arg:
        slug: key in Exercises dictionary for question/exercise ('q1', 'e1')

        Example:
        course_page.click_exercise(slug="q1")
        """
        with allure.step(f'User clicks on exercise "{slug}"'):
            exercise_id = self.get_exercise_id(slug)
            self.exercise_item.click(exercise_id=exercise_id)

    @with_iframe(BasePage.tool_iframe)
    def click_download_attachment(self, file_path_or_name: str):
        safe_file_name = file_name_or_path_resolve(file_path_or_name)
        self.answer_file_button.click(file_name=safe_file_name)

    def ui_course_link_is_visible(self):
        self.ui_course_link.is_visible()

    def ui_course_link_disappear(self):
        self.ui_course_link.disappear()

    def check_course_datetime(self, dt_format: DateTimeFormatters, dt_state: WorkflowDatetime):
        """
        Check that text with date and/or time present on page in expected format
        and return two objectives:
        workflow_datetime - date and time from DataBase for current workflow
        formatted_date - date and time in expected format by business design
        """
        workflow_datetime = Workflows.manager.get(workflow_id=self.learner['workflow_id'])[dt_state.value]

        formatted_date = datetime_format(dt=workflow_datetime, dt_format=dt_format)
        self.text_present(formatted_date, native=False)

        return formatted_date, workflow_datetime
