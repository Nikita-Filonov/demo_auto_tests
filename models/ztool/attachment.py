import uuid
from datetime import datetime

from models_manager import Field, Model

from models.utils.utils import get_attachment_name, get_default_textbook_url
from models.ztool.answer import get_default_answer
from models.ztool.element import get_default_element
from settings import ZTOOL_DB_NAME
from utils.api.constants import DEFAULT_TEXTBOOK_ATTACHMENT


class AnswerAttachments(Model):
    database = ZTOOL_DB_NAME
    identity = 'answer_attachment_id'

    answer_attachment_id = Field(default=uuid.uuid4, json='id', category=str)
    answer_id = Field(default=get_default_answer, category=str)
    order = Field(default=0, json='order', category=int)
    name = Field(default=get_attachment_name, json='name', category=str)
    path = Field(default=DEFAULT_TEXTBOOK_ATTACHMENT, json='path', category=str)
    created: datetime = Field(default=datetime.now)
    created_by_user_id = Field(default=uuid.uuid4)
    modified: datetime = Field(default=datetime.now)
    modified_by_user_id = Field(default=uuid.uuid4)

    def __str__(self):
        return f'<AnswerAttachment {self.answer_attachment_id}>'


class ElementTextbookAttachments(Model):
    database = ZTOOL_DB_NAME
    identity = 'element_textbook_attachment_id'

    element_textbook_attachment_id = Field(default=uuid.uuid4, json='id', category=str)
    element_id = Field(default=get_default_element, category=str)
    order = Field(default=0, json='order', category=int)
    name = Field(default=get_attachment_name, json='name', category=str)
    url = Field(default=get_default_textbook_url, json='url', category=str)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    modified = Field(default=datetime.now, category=str)
    modified_by_user_id = Field(default=uuid.uuid4, category=str)

    def __str__(self):
        return f'<ElementTextbookAttachment {self.element_textbook_attachment_id}>'


class AnswerFeedbackAttachments(Model):
    database = ZTOOL_DB_NAME
    identity = 'answer_feedback_attachment_id'

    answer_feedback_attachment_id = Field(default=uuid.uuid4, json='id', category=str)
    answer_id = Field(default=get_default_answer, category=str)
    order = Field(default=0, json='order', category=str)
    name = Field(default=get_attachment_name, json='name', category=str)
    path = Field(default=DEFAULT_TEXTBOOK_ATTACHMENT, json='path', category=str)
    created = Field(default=datetime.now, category=str)
    created_by_user_id = Field(default=uuid.uuid4, category=str)
    modified = Field(default=datetime.now, category=str)
    modified_by_user_id = Field(default=uuid.uuid4, category=str)

    def __str__(self):
        return f'<AnswerFeedbackAttachment {self.answer_feedback_attachment_id}>'
