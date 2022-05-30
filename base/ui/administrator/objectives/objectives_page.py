from enum import Enum

from pylenium.driver import Pylenium

from base.ui.administrator.administrator_page import AdministratorPage
from base.ui.author.course_details import CourseDetailsPage
from base.ui.base_page import BasePage
from base.ui.login_page import UsersViews
from models.users.activity import Activities, SupportedLTIVersion
from models.users.objective import Objectives
from models.utils.utils import get_code
from parameters.courses.ui.context import context_template
from utils.ui.components.button import Button
from utils.ui.components.form import Form
from utils.ui.components.iframe import with_iframe
from utils.ui.components.input import Input
from utils.ui.components.item import Item
from utils.ui.components.menu import Menu
from utils.ui.components.text import Text
from utils.utils import wait, random_string


class ObjectiveAdminLTIVersion(Enum):
    LTI_1_1 = "LTI 1.1", 1
    LTI_1_3 = "LTI 1.3", 2


class ObjectiveAdministrationPage(AdministratorPage):
    objectives_title = Text('//*[@data-qa="objectives-title"]', 'Objectives')
    create_new_objective_button = Button('//*[@data-qa="create-new-button"]', 'Create new')
    create_new_text_button = Button('//*[@data-qa="create-new-text-button"]', 'Create new text')
    open_tool_button = Button('//*[@data-qa="open-tool-button"]', 'Open tool')
    create_objective_title = Text('//*[@data-qa="create-objective-title"]', 'Create objective')
    name_input = Input('//input[@name="name"]', 'Name', random_string)
    code_input = Input('//input[@name="code"]', 'Code', get_code)
    activity_tool_url_input = Input('//input[@name="activity.toolUrl"]', 'URL', Activities.tool_url.get_default)
    activity_tool_resource_id_input = Input('//input[@name="activity.toolResourceId"]', 'Resource ID',
                                            Activities.tool_resource_id.get_default)
    description_input = Input('//textarea[@name="description"]', 'Description', Objectives.description.get_default)
    lti_version_input = Input('//input[@name="activity.ltiVersion"]', 'LTI version')
    lti_version_menu = Menu('//*[@data-qa="lti-version-menu"]', 'LTI version')
    lti_version_item = Item('(//*[@class="dx-item-content dx-list-item-content"])[{version_index}]', 'LTI version')

    objective_form = Form([name_input, code_input, activity_tool_url_input,
                           activity_tool_resource_id_input, description_input])

    def __init__(self, py: Pylenium, context):
        super().__init__(py)
        self.py = py
        self.context = context
        self.course_details = CourseDetailsPage(py, context=context_template)

    def visit_entity(self):
        wait(
            lambda: Objectives.manager.filter(name=self.name_input.cached_value, as_json=False).count() > 0,
            waiting_for=f'Until objective with name "{self.name_input.cached_value}" exists'
        )
        objective = Objectives.manager.get(name=self.name_input.cached_value)
        url = UsersViews.OBJECTIVE_PAGE.value.format(objective_id=objective['objective_id'])
        self.py.visit(url)

    def set_value_from_lti_menu(self, lti_version: ObjectiveAdminLTIVersion):
        """
        Select LTI version from dropdown menu

        :arg:
        lti_version: value from class ObjectiveAdminLTIVersion

        Example:
        objective_page.set_value_from_lti_menu(SupportedLTIVersion.LTI_1_1)
        """
        _, version_index = lti_version.value
        self.lti_version_menu.click()
        self.lti_version_item.click(version_index=version_index)

    def check_value_in_lti_menu(self, lti_version: SupportedLTIVersion):
        self.lti_version_input.have_value(lti_version.value)

    @with_iframe(BasePage.tool_iframe)
    def check_open_tool(self):
        self.course_details.editor_tab.is_visible()
