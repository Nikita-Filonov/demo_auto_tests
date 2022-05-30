from pylenium.driver import Pylenium

from base.ui.administrator.administrator_page import AdministratorPage
from base.ui.login_page import UsersViews
from models.users.group import Groups
from utils.ui.components.button import Button
from utils.ui.components.form import Form
from utils.ui.components.input import Input
from utils.ui.components.tab import Tab
from utils.ui.components.text import Text


class AdministratorGroupsPage(AdministratorPage):
    groups_title = Text('//*[@data-qa="groups-title"]', 'Groups title')
    create_group_title = Text('//*[@data-qa="create-group-title"]', 'Create group title')
    create_group_button = Button('//*[@data-qa="create-group-button"]', 'Create group')
    name_input = Input('//input[@name="name"]', 'Name', Groups.name.get_default)
    group_form = Form([name_input])

    users_tab = Tab('//*[@data-qa="users-tab"]', 'Users')
    owners_tab = Tab('//*[@data-qa="owners-tab"]', 'Owners')
    add_owner_button = Button('//*[@data-qa="add-owner-button"]', 'Add owner')

    def __init__(self, py: Pylenium, context):
        super().__init__(py)
        self.py = py
        self.context = context

    def visit_entity(self):
        group = Groups.manager.get(name=self.name_input.value)
        url = UsersViews.ADMINISTRATOR_GROUPS_FORM.value.format(group_id=group['group_id'])
        self.py.visit(url)

    def user_present_in_gird(self, user: dict = None):
        safe_user = user or self.context['user']
        try:
            self.text_present(safe_user['email'])
        except KeyError:
            self.text_present(safe_user['username'])
        self.text_present(safe_user['last_name'])
        self.text_present(safe_user['first_name'])
