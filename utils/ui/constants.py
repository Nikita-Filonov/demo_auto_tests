import os
from enum import Enum

from settings import PROJECT_ROOT


class SupportedLanguages(Enum):
    """Supported languages"""
    EN = 'en-US'
    RU = 'ru-RU'


DOWNLOAD_PATH = os.path.join(PROJECT_ROOT, 'downloads')
INPUT_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
