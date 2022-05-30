from http import HTTPStatus
from typing import List, Union, Optional

from assertions import assert_response_status, assert_attr, validate_json, assert_all
from requests import Response

from models.users.grades import Grades
from models.users.grading_scale import GradingScales
from utils.utils import random_number, random_string

KEYS_TO_NORMALIZE = [Grades.max_score.json, Grades.name.json]


def get_max_grades_score(grades: List[dict]) -> int:
    """
    :param grades: List of models.users.grades.Grades
    :return: Will return max ``maxScore`` from the grades list
    """
    return max(grades, key=lambda g: g[Grades.max_score.json])[Grades.max_score.json]


def normalized_grading_scales_grades(number_of_grades: int, keys: List[str] = None) -> List[dict]:
    """
    :param number_of_grades: Number of grades which we are want to generate
    :param keys: List of keys which should be unique. If some of the generated
    grades will have repeated keys, then we will regenerate grades again, until
    all the keys will not become unique
    :return: List of grades
    """
    safe_grades = [Grades.manager.to_json for _ in range(number_of_grades)]
    for key in (keys or KEYS_TO_NORMALIZE):
        mapped_keys = [grade[key] for grade in safe_grades]
        if len(mapped_keys) != len(set(mapped_keys)):
            return normalized_grading_scales_grades(number_of_grades, keys)

    return safe_grades


def denormalized_grading_scales_grades(number_of_grades: int, max_score: Optional[Union[int]] = None) -> List[dict]:
    """
    :param max_score: Override static max score value
    :param number_of_grades: Number of grades which we are want to generate
    :return: Will return list of grades, where ``name``, ``maxScore`` are negative values
    """
    static_name = random_string()
    static_max_score = random_number() if max_score is None else max_score
    return [
        {**Grades.manager.to_json, Grades.name.json: static_name, Grades.max_score.json: static_max_score}
        for _ in range(number_of_grades)
    ]


def check_grading_scales_response(grading_scale_response: Response, grading_scale_payload: dict):
    """
    :param grading_scale_response: Grading scale response which should contains info about grading scale.
    For example json of such response might look like:
    {
        'id': '8065c237-94cd-43fe-8b93-bf5913acb1d7',
        'name': 'wH6LbYE6syEoCnvwoGIkVWUbyatCcHSFTAOMstHuC80wVbs',
        'maxScore': 46,
        'numberOfGrades': 4,
        'grades': [
            {'name': 'cKUv4veVFTcrw7B9ECHsNxDloNAMMstYWTTu5yUV', 'maxScore': 32, 'color': '#0D4C5E'},
            {'name': 'ym8RoxMWuE5iVPgnphxjCeoHi59tf', 'maxScore': 31, 'color': '#3EDF91'},
            {'name': 'oQUlTwKnnvvcFWQccr0d7mjZG3e78gORVhZag', 'maxScore': 34, 'color': '#E67379'},
            {'name': '9Kqom2OYrGRuDbVZKShvxLiPaFthe7EFYvPK32EOY0rY2Oyh9', 'maxScore': 46, 'color': '#6A3E8B'}
        ]
    }

    :param grading_scale_payload: Dictionary with grading scale properties. You can get this payload from
    GradingScales model, ``GradingScales.manager.to_json``
    :return:

    Can be used to check grading scale response. Will check status code, schema, and all properties
    """
    json_response = grading_scale_response.json()
    max_score = get_max_grades_score(json_response[GradingScales.grades.json])

    assert_response_status(grading_scale_response.status_code, HTTPStatus.OK)
    assert_attr(json_response[GradingScales.name.json], grading_scale_payload[GradingScales.name.json],
                GradingScales.name.json)
    assert_attr(
        json_response[GradingScales.number_of_grades.json],
        len(grading_scale_payload[GradingScales.grades.json]),
        GradingScales.number_of_grades.json
    )
    assert_all(
        json_response[GradingScales.grades.json],
        grading_scale_payload[GradingScales.grades.json],
        'List of grades',
        [Grades.name.json, Grades.max_score.json, Grades.color.json]
    )
    assert_attr(json_response[GradingScales.max_score.json], max_score, GradingScales.max_score.json)
    validate_json(json_response, GradingScales.manager.to_schema)
    validate_json(json_response[GradingScales.grades.json], Grades.manager.to_array_schema)
