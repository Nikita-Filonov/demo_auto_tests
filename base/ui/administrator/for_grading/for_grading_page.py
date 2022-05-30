from base.ui.administrator.administrator_page import AdministratorPage
from utils.ui.components.iframe import without_iframe
from utils.ui.components.text import Text


class ForGradingPageLocators:
    for_grading_title = Text('//*[@data-qa="for-grading-title"]', "For Grading")


class ForGradingPage(AdministratorPage, ForGradingPageLocators):
    def __init__(self, py):
        super().__init__(py)

    @without_iframe(AdministratorPage.tool_iframe)
    def for_grading_title_should_be_visible(self):
        return self.for_grading_title.is_visible()
