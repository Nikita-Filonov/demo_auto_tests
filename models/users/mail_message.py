import uuid
from datetime import datetime

from models_manager import Field, Model

from settings import USERS_DB_NAME, DEFAULT_TENANT
from utils.utils import random_string


class MailMessages(Model):
    SCOPE = [
        {'name': 'MailMessage.Read', 'scope': None, 'scopeType': None},
        {'name': 'MailMessage.Delete', 'scope': None, 'scopeType': None},
        {'name': 'MailMessage.Update', 'scope': None, 'scopeType': None},
        {'name': 'MailMessage.Create', 'scope': None, 'scopeType': None},
    ]
    database = USERS_DB_NAME
    identity = 'mail_message_id'

    mail_message_id = Field(default=uuid.uuid4, json='id', category=str)
    state = Field(default=0, json='state', category=int)
    text_body = Field(default=random_string, json='textBody', category=str)
    html_body = Field(default=random_string, json='htmlBody', category=str)
    to_name = Field(default=random_string, json='toName', category=str)
    to_address = Field(default=random_string, json='toAddress', category=str)
    tenant_id = Field(default=DEFAULT_TENANT['id'], json='tenantId', category=str, is_related=True)
    subject = Field(default=random_string, json='subject', category=str)
    created = Field(default=datetime.now, category=str)
    modified = Field(default=datetime.now, category=str)

    def __str__(self):
        return f'<MailMessage {self.mail_message_id}>'
