import uuid

from models_manager import Field, Model

from settings import USERS_DB_NAME, DEFAULT_USER
from utils.utils import random_string


class DataGridSettings(Model):
    SCOPE = [
        {'name': 'DataGridSettings.Read', 'scope': None, 'scopeType': None},
        {'name': 'DataGridSettings.Delete', 'scope': None, 'scopeType': None},
        {'name': 'DataGridSettings.Update', 'scope': None, 'scopeType': None},
        {'name': 'DataGridSettings.Create', 'scope': None, 'scopeType': None},
    ]
    database = USERS_DB_NAME
    identity = 'data_grid_setting_id'

    data_grid_setting_id = Field(default=uuid.uuid4, json='id', category=str)
    user_id = Field(default=DEFAULT_USER['id'], json='userId', is_related=True, category=str, optional=True)
    key = Field(default=random_string, json='key', category=str)
    settings = Field(default=random_string, json='settings', category=str)

    def __str__(self):
        return f'<DataGridSettings {self.data_grid_setting_id}>'
