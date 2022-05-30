from datetime import datetime
from time import sleep
from typing import List, Dict, Union

import allure
import arrow
from arrow import Arrow
from dateutil import tz

from settings import LANGUAGE
from utils.formatters.dates import DateTimeFormatters
from utils.ui.constants import SupportedLanguages


def normalized_grades(grades: List[Dict]):
    """
    Based on
    normalizedGrades() {
        const sortedGrades: IGrade[] = [...this.grades].sort((a, b) => b.max - a.max);

        return sortedGrades.map((g, i) => {
            const nextMaxScore = sortedGrades[i + 1]?.max ?? -1;

            return { ...g, min: nextMaxScore + 1 };
        });
    }
    :return:
    """
    sorted_grades = sorted(grades, key=lambda g: g['max'], reverse=True)

    return [
        {
            **grade,
            'min': (-1 if (len(grades) <= index + 1) else sorted_grades[index + 1]['max']) + 1
        }
        for index, grade in enumerate(sorted_grades)
    ]


def get_grade_class(exercise_max_score, answer_score):
    """
    Based on

    get gradeClass() {
        const percent = this.exercise.maxScore && this.answer.score != null
            ? (this.answer.score / this.exercise.maxScore) * 100
            : 100;
        if (percent >= 80) {
            return 'text-success';
        }
        if (percent >= 40) {
            return 'text-warning';
        }

        return 'text-danger';
    }
    """
    percent = (answer_score / exercise_max_score) * 100 if (exercise_max_score and answer_score is not None) else 100
    if percent >= 80:
        return 'text-success'

    if percent >= 40:
        return 'text-warning'

    return 'text-danger'


def wait_for(seconds: int, waiting_for: str):
    """
    Wrapper around ``sleep``. Not recommended to use,
    but if need wait without any condition, then it should
    be used.
    """
    with allure.step(f'Waiting {seconds} seconds {waiting_for}'):
        sleep(seconds)


def datetime_format(dt: Union[Arrow, datetime] = None,
                    dt_format: DateTimeFormatters = DateTimeFormatters.COMMON_SHORT_DATE_WITH_TIME_FORMAT,
                    locale: SupportedLanguages = None) -> str:
    """
    :param dt: datetime or Arrow object
    :param dt_format: any of supported ``DateTimeFormatters``
    :param locale: any of ``SupportedLanguages``
    :return: formatted ``dt`` with given locale and format template

    Can be used to format date with given template and locale

    Example:
        now = datetime.now() -> datetime.datetime(2021, 12, 02, 12, 15, 42, 849856)
        format = DateTimeFormatters.COMMON_SHORT_DATE_WITH_TIME_FORMAT -> 'MM/DD/YYYY HH:mm'
        locale = SupportedLanguages.EN -> 'en-Us'

        datetime_format(now, format, locale) -> '12/2/2021 12:15'
    """
    # handle python datetime and convert it to arrow
    if isinstance(dt, datetime):
        dt = arrow.get(dt)

    # if no datetime provided then just use current datetime
    # and then converting this datetime to local datetime
    safe_dt = (dt or arrow.now()).to(tz=tz.tzlocal())

    # if no locale provided then just use locale from settings
    safe_locale = (locale or SupportedLanguages(LANGUAGE)).value
    dt_format = dt_format.value[safe_locale]

    # if dt_format is tuple or list
    if isinstance(dt_format, (tuple, list)):
        # then we should handle formatting for this case
        # splitting dt_format, into actual datetime format and parts
        dt_format, parts = dt_format[0], dt_format[1:]

        # returning formatted datetime and applying parts
        return safe_dt.format(dt_format, locale=safe_locale).format(*parts)

    return safe_dt.format(dt_format, locale=safe_locale)
