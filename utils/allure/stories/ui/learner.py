from enum import Enum


class CoursesStory(Enum):
    COURSE_FINISHED = 'Course state: finished'
    COURSE_NOT_STARTED = 'Course state: not started'
    COURSE_IN_PROGRESS = 'Course state: in progress'
    COURSE_SUBMITTED = 'Course state: submitted'
    COURSE_IN_GRADING = 'Course state: in grading'


class LearnerProfile(Enum):
    LEARNER_PROFILE = 'Learner profile'
