from pylenium.driver import Pylenium

from base.ui.administrator.administrator_page import AdministratorPage
from base.ui.login_page import UsersViews
from models.users.role_pattern import RolePatterns
from utils.ui.components.button import Button
from utils.ui.components.form import Form
from utils.ui.components.input import Input
from utils.ui.components.text import Text
from utils.utils import random_string


class AdministratorRolePatternsPage(AdministratorPage):
    role_patterns_title = Text('//*[@data-qa="role-patterns-title"]', 'Role patterns')
    create_new_role_pattern_button = Button('//*[@data-qa="create-new-role-pattern-button"]', 'Create new role pattern')
    create_role_patterns_title = Text('//*[@data-qa="create-role-pattern-title"]', 'Create role pattern title')
    name_input = Input('//input[@name="name"]', 'Name', random_string)
    scope_type_input = Input('//input[@name="scopeType"]', 'Scope Type', random_string)

    create_role_pattern_form = Form([name_input, scope_type_input])
    update_role_pattern_form = Form([name_input])

    def __init__(self, py: Pylenium, context):
        super().__init__(py)
        self.py = py
        self.context = context

    def visit_entity(self):
        role_patterns = RolePatterns.manager.get(name=self.name_input.cached_value)
        url = UsersViews.ADMINISTRATOR_ROLE_PATTERN.value.format(role_pattern_id=role_patterns['role_pattern_id'])
        self.py.visit(url)
