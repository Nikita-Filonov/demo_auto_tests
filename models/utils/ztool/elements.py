from typing import List, Dict, Optional

from models.ztool.element import Elements, Grades
from models.ztool.exercise import Exercises
from utils.api.constants import DEFAULT_TEXTBOOK_ATTACHMENT_PATH
from utils.minio.storage import upload_to_storage


def create_element(element_payload: dict = None,
                   grades_payload: List[Dict] = None,
                   exercises_payload: List[Dict] = None) -> str:
    """
    Return element with custom properties.

    :param element_payload: properties from class Elements
    :param grades_payload: properties from class Grades
    :param exercises_payload: properties from class Exercises

    Example:

    def create_element(element_payload, grades_payload, exercises_payload)
    :return element_id -> '751055b8-e450-452e-9adb-8d08c8c6ee98'
    """
    safe_element_payload = element_payload or {}
    safe_grades_payload = grades_payload or []
    safe_exercises_payload = exercises_payload or []

    element_id = Elements.manager.create(**safe_element_payload, as_json=False).element_id.value
    for grade_payload in safe_grades_payload:
        Grades.manager.create(element_id=element_id, **grade_payload)

    for exercise_payload in safe_exercises_payload:
        Exercises.manager.create(element_id=element_id, **exercise_payload)

    return element_id


def upload_default_textbook_attachment(file_paths: Optional[List[str]] = None):
    """
    Used to upload files into s3 storage. So those files can be used later
    to download/upload.

    We need this because, we do not want to upload files for each tests,
    which need files. We want to upload file once, and then use him every where
    """
    safe_file_paths = [*(file_paths or []), DEFAULT_TEXTBOOK_ATTACHMENT_PATH]
    for file_path in safe_file_paths:
        upload_to_storage(file_path)
