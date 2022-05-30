from base.ui.administrator.resource_library.resource_library_page import AdministratorResourceLibraryPage
from models.users.resource_libraries import SupportedResourceLibraryType, SupportedResourceLibraryModel

lti_form_parameters = [
    {
        'type': SupportedResourceLibraryType.LTI_1_1,
        'form': AdministratorResourceLibraryPage.create_resource_library_LTI11_form,
        'model': SupportedResourceLibraryModel.LTI_1_1
    },
    {
        'type': SupportedResourceLibraryType.LTI_1_3,
        'form': AdministratorResourceLibraryPage.create_resource_library_LTI13_form,
        'model': SupportedResourceLibraryModel.LTI_1_3
    },
    {
        'type': SupportedResourceLibraryType.PUBLIC_FILE,
        'form': AdministratorResourceLibraryPage.create_resource_library_public_file_form,
        'model': SupportedResourceLibraryModel.PUBLIC_FILE
    },
    {
        'type': SupportedResourceLibraryType.PRIVATE_FILE,
        'form': AdministratorResourceLibraryPage.create_resource_library_private_file_form,
        'model': SupportedResourceLibraryModel.PRIVATE_FILE
    },
]
