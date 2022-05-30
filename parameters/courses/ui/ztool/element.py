from datetime import datetime, timedelta, time

from settings import PROJECT_ROOT

textbook = open(PROJECT_ROOT + '/parameters/courses/ui/course.html').read()
guideline = open(PROJECT_ROOT + '/parameters/courses/ui/guideline.html').read()
preferred_end_date = datetime.combine(datetime.now(), time.min) + timedelta(days=14)

element_properties = {
    "grading_start_date": datetime.combine(datetime.now(), time.min) + timedelta(days=1),
    "grading_end_date": preferred_end_date,
    "grade_disclosure_date": preferred_end_date,
    "min_bonus": -10,
    "max_bonus": 10,
    "textbook": textbook,
    "tutor_guideline": guideline
}
