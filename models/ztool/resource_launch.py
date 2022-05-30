import uuid
from datetime import datetime
from typing import Optional

from models_manager import Field, Model

from models.ztool.element import get_default_element
from settings import ZTOOL_DB_NAME, DEFAULT_USER
from utils.utils import random_string


class ResourceLaunches(Model):
    database = ZTOOL_DB_NAME
    identity = 'resource_launch_id'

    resource_launch_id = Field(default=uuid.uuid4, category=str, json='id')
    element_id = Field(default=get_default_element, category=str, json='elementId')
    user_id = Field(default=DEFAULT_USER['id'], category=str, json='userId')
    context_id = Field(default=uuid.uuid4, category=str, json='contextId')
    resource_id = Field(default=uuid.uuid4, category=str, json='resourceId')
    sourced_id = Field(default=uuid.uuid4, category=Optional[str], json='sourcedId')
    line_item_url = Field(default=random_string, category=str, json='lineItemUrl')
    return_url = Field(default=random_string, category=str, json='returnUrl')
    roles = Field(default='Learner', category=str, json='roles')
    workflow_id = Field(default=uuid.uuid4, category=str, json='workflowId')
    created = Field(default=datetime.now)

    def __str__(self):
        return f'<ResourceLaunch {self.resource_launch_id}>'
