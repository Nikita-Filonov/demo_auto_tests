from base.ui.base_page import BasePage
from utils.ui.components.button import Button
from utils.ui.components.item import Item
from utils.ui.components.text import Text


class AdministratorPage(BasePage):
    """Base administrator page for common methods"""
    load_panel = Item('//div[@class="dx-loadpanel-content-wrapper"]', 'Load panel')
    create_form_title = Text('//*[@data-qa="create-form-title"]', 'Create form title')
    cancel_form_button = Button('//*[@data-qa="cancel-button"]', 'Cancel')
    create_form_button = Button('//*[@data-qa="create-button"]', 'Create')
    update_form_button = Button('//*[@data-qa="update-button"]', 'Update')

    def __init__(self, py):
        super().__init__(py)

    def click_create(self):
        self.create_form_button.click()
        self.load_panel.disappear()

    def click_update(self):
        self.update_form_button.click()
        self.load_panel.disappear()

    def visit_entity(self):
        raise NotImplementedError(
            'You have to override "visit_entity" method '
            'inside you page object, if you want ti use it'
        )
