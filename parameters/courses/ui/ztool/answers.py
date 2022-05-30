from parameters.courses.ui.ztool.exercises import exercises_properties
from utils.utils import random_string

answers_properties = [
    {"text": random_string(), "feedback": random_string(), "score": exercise['max_score']}
    for exercise in exercises_properties
]

answers_null_properties = [{'text': random_string(), 'feedback': None, 'score': None} for _ in exercises_properties]
