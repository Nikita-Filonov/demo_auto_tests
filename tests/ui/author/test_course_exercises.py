import allure
import pytest

from parameters.courses.ui.ztool.exercises import exercises_properties
from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.author import AuthorStory


@allure.issue(
    url='https://youtrack.alemira.dev/issue/ALMS-953',
    name='[Author] User not redirected back to course edit after adding an exercise'
)
@pytest.mark.ui
@pytest.mark.exercises
@pytest.mark.author_course_exercises
@allure.epic('Core LMS')
@allure.feature('Author (UI)')
@allure.story(AuthorStory.COURSE_EXERCISES.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestExercisesUi:
    EXERCISE = exercises_properties[0]

    @allure.id("3991")
    @allure.title('Create exercise (UI)')
    def test_create_exercise(self, new_exercise):
        new_exercise.click_add_exercise()
        new_exercise.exercise_form.fill()
        new_exercise.click_add_exercise()
        new_exercise.click_exercise_group_collapse(new_exercise.group_input.cached_value)
        new_exercise.text_present(new_exercise.slug_input.cached_value)

    @allure.id("3990")
    @allure.title('Edit exercise (UI)')
    def test_edit_exercise(self, new_exercise):
        new_exercise.click_exercise_group_collapse(self.EXERCISE['group'])
        new_exercise.click_exercise_link(self.EXERCISE['slug'])
        new_exercise.exercise_form.fill()
        new_exercise.click_update_exercise()
        new_exercise.click_exercise_group_collapse(new_exercise.group_input.cached_value)
        new_exercise.text_present(new_exercise.slug_input.cached_value)
