from typing import Dict, Optional, Union

from pylenium.driver import Pylenium

from base.ui.author.author_page import AuthorPage
from base.ui.base_page import BasePage
from models.users.activity import Activities
from models.users.objective import Objectives
from utils.ui.components.button import Button
from utils.ui.components.iframe import without_iframe
from utils.ui.components.item import Item
from utils.ui.components.text import Text


class CoursesPage(AuthorPage):
    card_title = Item('//*[@data-qa="card-title-{course_id}"]', 'Card title')
    my_courses_title = Text('//*[@data-qa="my-courses-title"]', 'My courses')
    logo_button = Button('//*[@data-qa="logo-learner-button"]', 'Logo')

    def __init__(self, py: Pylenium, context: Optional[Dict[str, Union[dict, list]]] = None):
        super().__init__(py, context)
        self.py = py
        self.context = context
        self.objective = self.context['objective']

    def click_course_card(self):
        self.card_title.click(course_id=self.objective[Objectives.objective_id.json])

    def course_title_present(self):
        self.text_present(self.objective['activity'][Activities.name.json])

    @without_iframe(BasePage.tool_iframe)
    def is_courses_page_location(self):
        self.my_courses_title.is_visible()
