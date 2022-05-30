import os
from http import HTTPStatus

from models_manager import FieldGenericEnum

from settings import PROJECT_ROOT

RESPONSE = 'response'
FORBIDDEN_RESPONSE = HTTPStatus.FORBIDDEN

DEFAULT_TEXTBOOK_ATTACHMENT = 'textbook.pdf'
DEFAULT_TEXTBOOK_ATTACHMENT_PATH = os.path.join(PROJECT_ROOT, f'parameters/courses/ui/{DEFAULT_TEXTBOOK_ATTACHMENT}')

GRID_PAGE_SIZES = [5, 10, 20]


class APIState(FieldGenericEnum):
    """
    API response state

    Some of responses contains response state:
    1 - means success
    2 - means error
    """
    SUCCESS = 1
    FAILED = 2
