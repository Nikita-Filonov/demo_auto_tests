import pytest

from base.api.ztool.element import upload_textbook_attachment_to_element, get_element
from models.ztool.attachment import ElementTextbookAttachments
from models.ztool.exercise import Exercises


@pytest.fixture(scope='function')
def element_with_exercises(request, launch):
    """
    Wrapper for adding exercises to a standard ``Element``.
    Add "count" parameter to change the number of added exercises.

    Example:

    @pytest.mark.parametrize('element_with_exercises', [{'count': 5}], indirect=['element_with_exercises'])
    def test_some(element_with_exercises):
        ...

    In this case ``element_with_exercises`` will return element with 5 exercises.
    """
    safe_count = request.param['count'] if hasattr(request, 'param') else 1

    exercises = [Exercises.manager.create(element_id=launch['element_id']) for _ in range(safe_count)]
    return {
        **launch,
        'data': exercises
    }


@pytest.fixture(scope='function')
def element_with_textbook_attachment(launch) -> dict:
    """
    Will return element with attached ``textbook-attachment``.
    Add list of parameters to change the file type dynamically.

    Example:

    @pytest.mark.parametrize(
        'element_with_textbook_attachment',
        [
            'parameters/files/some.png',
            'parameters/files/some.doc',
            'parameters/files/some.docx',
        ],
        indirect=['element_with_textbook_attachment']
    )
    def test_some(element_with_textbook_attachment):
        ...

    In this case autotest will run 3 times with 3 different types.
    ``element_with_exercises`` at first iteration will return
    element with attached 'some.png', then 'some.doc' etc.
    """
    textbook_payload = ElementTextbookAttachments.manager.to_dict()
    upload_textbook_attachment_to_element(launch['request_id'], launch['element_id'], textbook_payload)

    element_payload = get_element(launch['request_id'], launch['element_id']).json()

    if element_payload.get('textbookAttachments') is None:
        pytest.fail(f'Unable to attach file "{textbook_payload}". "Element": {element_payload}\n'
                    f'Make sure you are using right role for that purpose. Current role is: {launch["role"]}')

    if len(element_payload['textbookAttachments']) == 0:
        pytest.fail(f'Unable to attach file "{textbook_payload}". "Element": {element_payload}')

    return {
        'data': element_payload,
        'textbook_payload': textbook_payload,
        **launch
    }
