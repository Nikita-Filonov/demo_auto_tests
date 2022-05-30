from pylenium.driver import Pylenium

from base.ui.administrator.administrator_page import AdministratorPage
from base.ui.login_page import UsersViews
from models.users.tenant import Tenants
from utils.ui.components.button import Button
from utils.ui.components.form import Form
from utils.ui.components.input import Input
from utils.ui.components.text import Text
from utils.utils import random_string


class AdministratorTenantsPage(AdministratorPage):
    tenants_title = Text('//*[@data-qa="tenants-title"]', 'Tenants')
    create_new_tenant_button = Button('//*[@data-qa="create-new-tenant-button"]', 'Create new tenant')
    create_tenant_title = Text('//*[@data-qa="create-tenant-title"]', 'Create tenant title')
    name_input = Input('//input[@name="name"]', 'Name', random_string)
    last_name_input = Input('//input[@name="lastName"]', 'Last Name', Tenants.admin_user.get_default['lastName'])
    email_input = Input('//input[@name="email"]', 'Email', Tenants.admin_user.get_default['email'])

    create_tenant_form = Form([name_input, last_name_input, email_input])
    update_tenant_form = Form([name_input])

    def __init__(self, py: Pylenium, context):
        super().__init__(py)
        self.py = py
        self.context = context

    def visit_entity(self):
        tenant = Tenants.manager.get(name=self.name_input.cached_value)
        url = UsersViews.ADMINISTRATOR_TENANT.value.format(tenant_id=tenant['tenant_id'])
        self.py.visit(url)
