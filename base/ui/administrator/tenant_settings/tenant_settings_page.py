from pylenium.driver import Pylenium

from base.ui.administrator.administrator_page import AdministratorPage
from utils.ui.components.button import Button
from utils.ui.components.text import Text


class AdministratorTenantSettingPage(AdministratorPage):
    tenants_title = Text('//*[@data-qa="tenant-settings-title"]', 'Tenant settings')
    create_new_tenant_button = Button('//*[@data-qa="create-new-tenant-setting-button"]', 'Add new tenant setting')
    tenant_setting_name = Text('//*[@data-qa="{tenant_setting_id}-data0-column"]', 'Tenant setting name')
    tenant_setting_value = Text('//*[@data-qa="{tenant-setting-id}-data1-column"]', 'Tenant setting value')

    def __init__(self, py: Pylenium, context):
        super().__init__(py)
        self.py = py
        self.context = context
