from typing import Optional

from alms_integration import LTIActivities, TextActivity as LibTextActivity
from alms_integration import create_activity
from models_manager import Field, Model, FieldGenericEnum

from models.utils.utils import get_tool_resource_id
from settings import USERS_DB_NAME, Z_TOOL_API


class SupportedLTIVersion(FieldGenericEnum):
    LTI_1_1 = 1
    LTI_1_3 = 3
    NULL = None


class SupportedActivityType(FieldGenericEnum):
    TEXT = 1
    LTI = 2
    NULL = None


class Activities(LTIActivities):
    database = USERS_DB_NAME

    tool_url = Field(
        default=lambda: Z_TOOL_API + f'/launch/{get_tool_resource_id()}',
        json='toolUrl',
        category=Optional[str],
        max_length=2000,
        null=True
    )
    tool_resource_id = Field(
        default=get_tool_resource_id,
        json='toolResourceId',
        category=Optional[str],
        max_length=2000,
        null=True
    )


class TextActivity(LibTextActivity):
    pass


def get_default_activity(**kwargs):
    """Returns default activity"""
    payload = Activities.manager.to_json
    return create_activity({**payload, **kwargs}).json()['id']


class CreateActivities(Model):
    database = USERS_DB_NAME
    identity = 'create_activity_id'

    create_activity_id = Field(category=str)


class UpdateActivities(Model):
    database = USERS_DB_NAME
    identity = 'update_activity_id'

    update_activity_id = Field(category=str)
