import allure
import pytest

from parameters.courses.ui.ztool.grades import grade_properties
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.author import AuthorStory


@pytest.mark.ui
@pytest.mark.author_course_details
@allure.epic('Core LMS')
@allure.feature('Author (UI)')
@allure.story(AuthorStory.COURSE_DETAILS.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestCourseDetailsUi:

    @allure.id("3914")
    @allure.title('Check course details (UI)')
    def test_check_course_details(self, course_details):
        element = course_details.element

        course_details.textbook_textarea.have_value(element['textbook'])
        course_details.tutor_guidelines_textarea.have_value(element['tutor_guideline'])
        course_details.min_instructor_bonus_input.have_value(element['min_bonus'])
        course_details.max_instructor_bonus_input.have_value(element['max_bonus'])

    @allure.id("3913")
    @allure.title('Update course (UI)')
    def test_update_course_details(self, course_details):
        course_details.course_form.fill()
        course_details.click_update_course()
        course_details.course_form.validate()

    @allure.id("3968")
    @pytest.mark.parametrize('grade', grade_properties)
    def test_author_check_grades(self, course_details, grade):
        allure.dynamic.title(f'Check value grades with "{grade}" (UI)')
        course_details.grade_input_value_equals(grade['name'], grade['max'])

    @allure.id("3988")
    @pytest.mark.parametrize('grade', [
        {'name': grade_properties[0]['name'], 'value': 12, 'expected': '12'},
        {'name': grade_properties[0]['name'], 'value': -12, 'expected': '-12'}
    ])
    def test_update_grades(self, course_details, grade):
        allure.dynamic.title(f'Update grades with grade "{grade["value"]}" (UI)')
        course_details.clear_grade_input(grade['name'])
        course_details.fill_grade(grade['name'], grade['value'])
        course_details.click_update_course()
        course_details.grade_input_value_equals(grade['name'], grade['expected'])

    @allure.id("3989")
    @allure.title('Update grades negative (UI)')
    @pytest.mark.parametrize('grade', [{'name': grade_properties[0]['name'], 'value': 0}])
    def test_update_grades_negative(self, course_details, grade):
        course_details.clear_grade_input(grade['name'])
        course_details.fill_grade(grade['name'], grade['value'])
        course_details.click_update_course()
        course_details.error_alert_present()

    @allure.id("4229")
    @allure.title('Author preview course (UI)')
    def test_author_preview_course(self, course_details):
        course_details.preview_course_button.click()
        course_details.go_to_course_edit_button.is_visible()
        course_details.text_present(course_details.COURSE_TITLE)
