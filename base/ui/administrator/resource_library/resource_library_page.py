from typing import List, Union, Dict

from pylenium.driver import Pylenium

from base.ui.administrator.administrator_page import AdministratorPage
from base.ui.login_page import UsersViews
from models.users.resource_libraries import SupportedResourceLibraryType, ResourceLibraries, \
    SupportedResourceLibraryModel
from utils.ui.components.button import Button
from utils.ui.components.checkbox import Checkbox
from utils.ui.components.form import Form
from utils.ui.components.input import Input
from utils.ui.components.item import Item
from utils.ui.components.menu import Menu
from utils.ui.components.text import Text
from utils.utils import random_string


def get_resource_library_checkbox_locator(locator: str, **kwargs):
    """
    Use with dynamic locators to format them: add dynamic part to locator

    locator: element with xpath selector -> str
    dynamic part: hidden part before and shown after using element (ex.: click) -> str
    """
    return (locator + '//input').format(**kwargs)


def to_change_resource_library_payload(
        parameters: List[Dict[str, Union[SupportedResourceLibraryType, Form, SupportedResourceLibraryModel]]]
):
    """
    Use in parametrize to choose and change parameters

    parameters:
        SupportedResourceLibraryType: Resource Library type
        Form: UI form on web page
        SupportedResourceLibraryModel: Resource Library model

    Example:
        to_change_resource_library_payload(
        SupportedResourceLibraryType.LTI_1_1,
        AdministratorResourceLibraryPage.create_resource_library_LTI11_form,
        SupportedResourceLibraryModel.LTI_1_1
        )
    :return:
        [4,
        Form(
        [name_input, url_input, consumer_key_input, user_input, image_url_input,
         actions_api_url_input, secret_key_input, password_input, auth_url_input],
        [support_lti_review_checkbox, support_lti_authoring_checkbox,
         support_lti_grading_checkbox, allow_publishing_checkbox,
         allow_editing_checkbox]),
        class ResourceLibrariesLTI11
        ]
    """
    return [(parameter['model'].value[0], parameter) for parameter in parameters]


class AdministratorResourceLibraryPage(AdministratorPage):
    resource_library_title = Text('//*[@data-qa="resource-libraries-title"]', 'Resource libraries title')
    add_new_resource_library_button = Button('//*[@data-qa="add-button"]', 'Add new resource library')
    add_new_resource_library_title = Text('//*[@data-qa="resource-library-title"]', 'Add resource libraries title')

    name_input = Input('//input[@name="name"]', 'Name', random_string)
    url_input = Input('//input[@name="url"]', 'URL', random_string)
    consumer_key_input = Input('//input[@name="consumerKey"]', 'Consumer Key', random_string)
    user_input = Input('//input[@name="user"]', 'User', random_string)
    image_url_input = Input('//input[@name="imageUrl"]', 'Image URL', random_string)
    actions_api_url_input = Input('//input[@name="actionsApiUrl"]', 'Action API URL', random_string)
    secret_key_input = Input('//input[@name="secretKey"]', 'Secret Key', random_string)
    password_input = Input('//input[@name="password"]', 'Password', random_string)
    auth_url_input = Input('//input[@name="authUrl"]', 'Auth URL', random_string)
    bucket_name_input = Input('//input[@name="bucketName"]', 'Bucket Name', random_string)
    subfolder_input = Input('//input[@name="subfolder"]', 'Subfolder', random_string)

    support_lti_review_checkbox = Checkbox('//*[@data-qa="support-lti-review-checkbox"]', 'Support Lti Review')
    support_lti_authoring_checkbox = Checkbox('//*[@data-qa="support-lti-authoring-checkbox"]', 'Support Lti Authoring')
    support_lti_grading_checkbox = Checkbox('//*[@data-qa="support-lti-grading-checkbox"]', 'Support Lti Grading')
    allow_publishing_checkbox = Checkbox('//*[@data-qa="allow-publishing-checkbox"]', 'Allow Publishing')
    allow_editing_checkbox = Checkbox('//*[@data-qa="allow-editing-checkbox"]', 'Allow Editing')

    lti_version_input = Input('//input[@name="type"]', 'Type')
    lti_version_menu = Menu('//*[@data-qa="type-select"]', 'Type select')
    lti_version_item = Item('(//*[@class="dx-item-content dx-list-item-content"])[text()="{version}"]',
                            'LTI version')

    create_resource_library_LTI11_form = Form(
        [name_input, url_input, consumer_key_input, user_input, image_url_input,
         actions_api_url_input, secret_key_input, password_input, auth_url_input],
        [support_lti_review_checkbox, support_lti_authoring_checkbox,
         support_lti_grading_checkbox, allow_publishing_checkbox,
         allow_editing_checkbox]
    )
    create_resource_library_LTI13_form = Form(
        [name_input, url_input, user_input, image_url_input,
         actions_api_url_input, password_input, auth_url_input],
        [support_lti_review_checkbox, support_lti_authoring_checkbox,
         support_lti_grading_checkbox, allow_publishing_checkbox,
         allow_editing_checkbox]
    )
    create_resource_library_public_file_form = Form(
        [name_input, url_input, user_input, image_url_input, password_input,
         bucket_name_input, subfolder_input],
        [allow_publishing_checkbox, allow_editing_checkbox]
    )
    create_resource_library_private_file_form = Form(
        [name_input, url_input, user_input, image_url_input,
         password_input, bucket_name_input, subfolder_input],
        [allow_publishing_checkbox, allow_editing_checkbox]
    )

    def __init__(self, py: Pylenium, context):
        super().__init__(py)
        self.py = py
        self.context = context

    def visit_entity(self):
        resource_library = ResourceLibraries.manager.get(name=self.name_input.cached_value)
        url = UsersViews.RESOURCE_LIBRARY_PAGE.value.format(resource_library_id=resource_library['resource_library_id'])
        self.py.visit(url)

    def set_value_from_lti_menu(self, lti_version: SupportedResourceLibraryModel):
        """
        Select LTI version from dropdown menu

        :arg:
        lti_version: value from class ObjectiveAdminLTIVersion

        Example:
        objective_page.set_value_from_lti_menu(SupportedResourceLibraryType.LTI_1_1)
        """
        _, version = lti_version.value
        self.lti_version_menu.click()
        self.lti_version_item.name = version
        self.lti_version_item.click(version=version)

    def check_value_in_lti_menu(self, lti_version: SupportedResourceLibraryType):
        version_index = lti_version.value
        self.lti_version_input.have_value(version_index)
