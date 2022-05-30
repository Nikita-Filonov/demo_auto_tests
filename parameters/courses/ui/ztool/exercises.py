from settings import PROJECT_ROOT

exercise1 = open(PROJECT_ROOT + '/parameters/courses/ui/exercises/exercise1.html').read()
exercise2 = open(PROJECT_ROOT + '/parameters/courses/ui/exercises/exercise2.html').read()

exercises_properties = [
    {"group": "Задачи", "max_score": 2, "text": exercise1, "slug": "e1", "order": 0},
    {"group": "Задачи", "max_score": 3, "text": exercise2, "slug": "e2", "order": 1},
    {"group": "Контрольные вопросы", "max_score": 4, "text": exercise1, "slug": "q1", "order": 0},
    {"group": "Контрольные вопросы", "max_score": 5, "text": exercise2, "slug": "q2", "order": 1}
]
