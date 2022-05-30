from datetime import datetime
from typing import Dict, Union

import allure
import pytest

from base.ui.author.course_details import CourseDetailsPage
from models.ztool.workflow import WorkflowStates
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.author import AuthorStory
from utils.ui.components.input import Input


@pytest.mark.ui
@pytest.mark.author_course_dates
@allure.epic('Core LMS')
@allure.feature('Author (UI)')
@allure.story(AuthorStory.COURSE_DATES.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestCourseDatesUi:

    @allure.id("4267")
    @allure.issue(
        url='https://youtrack.alemira.dev/issue/ALMS-1070',
        name='Objectives: Ztool: Dates: Validation message should be more informative"'
    )
    @pytest.mark.parametrize('payload', [
        {'locator': CourseDetailsPage.start_of_grading_date_input, 'value': datetime.now()},
        {'locator': CourseDetailsPage.end_of_grading_date_input, 'value': datetime.now()},
        {'locator': CourseDetailsPage.grading_disclosure_date_input, 'value': datetime.now()},
    ])
    def test_update_course_dates_on_course_details_page(self, course_dates, payload: Dict[str, Union[Input, str]]):
        allure.dynamic.title(f'Update course "{payload["locator"].name}" '
                             f'with value "{payload["value"]}" on course details page (UI)')
        payload['locator'].clear()
        payload['locator'].type(payload['value'])
        course_dates.click_update_course()
        payload['locator'].have_value(payload['value'])
        course_dates.error_alert_not_present()

    @allure.id("4268")
    @allure.title('Check course dates on course details page (UI)')
    def test_check_course_dates_on_course_details_page(self, course_dates):
        element = course_dates.element

        course_dates.start_of_grading_date_input.have_value(element['grading_start_date'])
        course_dates.end_of_grading_date_input.have_value(element['grading_end_date'])
        course_dates.grading_disclosure_date_input.have_value(element['grade_disclosure_date'])

    @allure.id("3917")
    @allure.title('Send all submitted courses to grading (UI)')
    def test_send_all_submitted_courses_to_grading(self, author_submitted_workflow):
        author_submitted_workflow.click_send_all_submitted_courses_to_grading_link(WorkflowStates.IN_GRADING)

    @allure.id("3960")
    @allure.title('Send all grading approved courses to finished link (UI)')
    def test_send_send_all_grading_approved_courses_to_finished_link(self, author_approved_workflow):
        author_approved_workflow.click_send_all_grading_approved_courses_to_finished_link(WorkflowStates.FINISHED)
