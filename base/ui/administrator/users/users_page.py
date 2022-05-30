from pylenium.driver import Pylenium

from base.ui.administrator.administrator_page import AdministratorPage
from base.ui.login_page import UsersViews
from models.users.user import Users
from utils.ui.components.button import Button
from utils.ui.components.form import Form
from utils.ui.components.input import Input
from utils.ui.components.text import Text
from utils.utils import wait


class AdministratorUsersPage(AdministratorPage):
    users_title = Text('//*[@data-qa="users-title"]', 'Users title')
    create_user_title = Text('//*[@data-qa="create-user-title"]', 'Create user title')
    create_user_button = Button('//*[@data-qa="create-user-button"]', 'Create user')
    first_name_input = Input('//input[@name="firstName"]', 'First name', Users.first_name.get_default)
    middle_name_input = Input('//input[@name="middleName"]', 'Middle name', Users.middle_name.get_default)
    last_name_input = Input('//input[@name="lastName"]', 'Last name', Users.last_name.get_default)
    email_input = Input('//input[@name="email"]', 'Email', Users.email.get_default)
    city_input = Input('//input[@name="details.city"]', 'City')
    school_input = Input('//input[@name="details.school"]', 'School')
    grade_input = Input('//input[@name="details.grade"]', 'Grade')
    user_form = Form([first_name_input, middle_name_input, last_name_input, email_input])

    def __init__(self, py: Pylenium, context):
        super().__init__(py)
        self.py = py
        self.context = context

    def visit_entity(self):
        wait(
            lambda: Users.manager.filter(email=self.email_input.value, as_json=False).count() > 0,
            waiting_for=f'Until user with email "{self.email_input.value}" exists'
        )
        user = Users.manager.get(email=self.email_input.value)
        url = UsersViews.ADMINISTRATOR_USERS_FORM.value.format(user_id=user['user_id'])
        self.py.visit(url)
