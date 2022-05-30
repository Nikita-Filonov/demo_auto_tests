from typing import Dict, Union

import allure

from base.ui.learner.courses.courses import CoursesPage
from models.ztool.workflow import WorkflowDatetime
from utils.formatters.dates import DateTimeFormatters
from utils.ui.components.button import Button
from utils.ui.components.iframe import without_iframe
from utils.ui.components.input import Input
from utils.ui.components.item import Item
from utils.ui.components.row import Row


class ProfilePage(CoursesPage):
    full_name_title = Item('//*[@data-qa="full-name-title"]', 'Full name')
    email_title = Item('//*[@data-qa="email-title"]', 'E-mail title')
    first_name = Input('//*[@data-qa="first-name-input"]', 'First name')
    middle_name = Input('//*[@data-qa="middle-name-input"]', 'Middle name')
    last_name = Input('//*[@data-qa="last-name-input"]', 'Last name')
    username = Input('//*[@data-qa="username-input"]', 'Username')
    email = Input('//*[@data-qa="email-input"]', 'E-mail')
    profile_back_button = Button('//*[@data-qa="profile-back-button"]', 'Back')
    row_score_to_max_score = Row('//*[@data-qa="row-score-to-max-score-{objective_id}"]', 'Score/Max Score')
    row_course_name = Row('//*[@data-qa="row-name-{objective_id}"]', 'Course name')
    row_course_date = Row('//*[@data-qa="row-date-{objective_id}"]', 'Course date')

    def __init__(self, py, context: Dict[str, Union[dict, list]]):
        super().__init__(py, context)
        self.py = py
        self.context = context

    @without_iframe(CoursesPage.tool_iframe)
    def click_profile_back(self):
        self.profile_back_button.click()

    @allure.step('Checking that grade and score are correct')
    def check_grade_and_score_on_profile_page(self):
        objective_id = self.objective['objective_id']
        grade_and_score_result = self.get_grade_and_score_result_value()

        self.row_score_to_max_score.is_visible(grade_and_score_result['correspondent_score'], objective_id=objective_id)
        self.row_grade.is_visible(grade_and_score_result['total_grade'], grade_id=objective_id)

    def row_course_name_contains_course_name(self):
        course_name = self.objective['name']
        objective_id = self.objective['objective_id']
        self.row_course_name.is_visible(course_name, objective_id=objective_id)

    def row_course_date_is_in_correct_format(self):
        objective_id = self.objective['objective_id']
        finished_date, _ = self.check_course_datetime(
            DateTimeFormatters.LEARNER_USER_PROFILE_LONG_DATE_FORMAT_WITH_TIME,
            WorkflowDatetime.FINISHED
        )
        self.row_course_date.is_visible(finished_date, objective_id=objective_id)
