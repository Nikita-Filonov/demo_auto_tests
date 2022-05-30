from enum import Enum

from utils.ui.constants import SupportedLanguages

EN = SupportedLanguages.EN.value
RU = SupportedLanguages.RU.value


class DateTimeFormatters(Enum):
    """
    Templates for formatting date/time/datetime

    For reference look in /code/frontend/(Learner/Author/Administration)/src/locales/
    """
    COMMON_SHORT_DATE_WITH_TIME_FORMAT = {EN: 'MM/DD/YYYY HH:mm', RU: 'DD.MM.YYYY HH:mm'}
    COMMON_SHORT_DATE_FORMAT = {EN: 'MM/D/YYYY', RU: 'D.MM.YYYY'}
    COMMON_SHORT_FULL_DATE_FORMAT = {EN: 'MM/DD/YYYY', RU: 'DD.MM.YYYY'}

    INSTRUCTOR_DATE_TIME_FORMAT = {EN: 'MM/DD/YYYY HH:mm', RU: 'DD MMMM YYYY г., в HH:mm'}

    LEARNER_COURSE_DETAILS_SHORT_DATE_FORMAT = {EN: 'MM/d/YYYY', RU: 'd.MM.YYYY'}
    LEARNER_COURSE_DETAILS_LONG_DATE_FORMAT_SAME_YEAR = {EN: 'MMMM d', RU: 'dd MMMM'}
    LEARNER_COURSE_DETAILS_LONG_DATE_FORMAT = {EN: 'MMMM d, YYYY', RU: 'd MMMM YYYY'}
    LEARNER_COURSE_DETAILS_SHORT_TIME_FORMAT = {EN: 'h:mm a', RU: 'H:mm'}
    LEARNER_COURSE_DETAILS_LONG_DATE_TIME_FORMAT = {EN: 'MMMM d YYYY, h:mm A', RU: 'd MMMM YYYY, H:mm'}
    LEARNER_SUBMISSION_DATE_TIME_FORMAT = {EN: ('MMMM DD, YYYY {0} HH:mm', 'at'), RU: 'DD.MM.YYYY г. в HH:mm'}

    LEARNER_USER_PROFILE_LONG_DATE_FORMAT_WITH_TIME = {EN: 'MMMM D, YYYY hh:mm A', RU: 'D MMMM YYYY HH:mm'}

    LEARNER_COURSE_CARD_LONG_DATE_FORMAT_SAME_YEAR = {EN: 'MMMM d', RU: 'dd MMMM'}
    LEARNER_COURSE_CARD_LONG_DATE_FORMAT = {EN: 'MMMM d, YYYY', RU: 'd MMMM YYYY'}
