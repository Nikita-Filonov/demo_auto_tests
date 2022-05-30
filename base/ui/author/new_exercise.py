from typing import Dict, Union

from pylenium.driver import Pylenium

from base.ui.author.course_details import CourseDetailsPage
from utils.ui.components.button import Button
from utils.ui.components.form import Form
from utils.ui.components.input import Input
from utils.ui.components.textarea import Textarea
from utils.utils import random_string, random_number


class NewExercisePage(CourseDetailsPage):
    slug_input = Input('//*[@data-qa="slug-input"]', 'Slug', random_string)
    text_textarea = Textarea('//*[@data-qa="text-textarea"]', 'Text', random_string)
    answer_textarea = Textarea('//*[@data-qa="answer-textarea"]', 'Answer', random_string)
    tutor_guidelines_textarea = Textarea('//*[@data-qa="tutor-guidelines-textarea"]', 'Tutor guidelines', random_string)
    max_score_input = Input('//*[@data-qa="max-score-input"]', 'Max score')
    group_input = Input('//*[@data-qa="group-input"]', 'Group', random_string)
    order_input = Input('//*[@data-qa="order-input"]', 'Order', random_number)
    add_exercise_button = Button('//*[@data-qa="add-exercise-button"]', 'Add exercise')
    update_exercise_button = Button('//*[@data-qa="update-exercise-button"]', 'Update exercise')

    exercise_form = Form([
        slug_input, text_textarea, answer_textarea,
        tutor_guidelines_textarea, group_input, order_input
    ])

    def __init__(self, py: Pylenium, context: Dict[str, Union[dict, list]]):
        super().__init__(py, context)
        self.py = py

    def click_add_exercise(self):
        self.add_exercise_button.click()

    def click_update_exercise(self):
        self.update_exercise_button.click()
