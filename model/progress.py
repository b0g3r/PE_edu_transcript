from collections import OrderedDict
from datetime import date, timedelta

from peewee import ForeignKeyField, IntegerField, BooleanField

from .base import BaseModel
from .student import Student
from .semester import Semester

class cached_property():
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        result = instance.__dict__[self.func.__name__] = self.func(instance)
        return result

def daterange(d1: date, d2: date):
    return (d1 + timedelta(days=i) for i in range((d2 - d1).days + 1))

class Progress(BaseModel):
    SEMESTER_TEST_PASSED = 2
    SEMESTER_TEST_READY = 1
    SEMESTER_TEST_NOT_READY = 0

    student = ForeignKeyField(Student)  # type: Student
    semester = ForeignKeyField(Semester)  # type: Semester
    required_exercises = IntegerField()  # type: int
    is_complete = BooleanField(default=False)  # type: bool

    def save(self, *args, **kwargs):
        self.required_exercises = self._get_default_count_of_exercises()
        return super().save(*args, **kwargs)

    def _get_default_count_of_exercises(self):
        course_number = (self.semester.start_date - date(self.student.group.admission_year, 9, 1)).days//365 + 1
        if course_number == 1:
            return 16
        elif course_number == 2:
            return 14
        elif course_number == 3:
            return 10
        elif course_number == 4:
            return 6

    @cached_property
    def visits(self) -> dict:

        visits = {}
        exercises = tuple(exercise.date for exercise in self.exercises)
        for day in daterange(self.semester.start_date, self.semester.end_date):
            visits[day] = exercises.count(day)
        return visits

    @cached_property
    def exams_result(self) -> dict:
        exams_result = {}
        for exam in self.semester.exams:
            exams_result[exam] = str(exam.get_result_for_progress(self))
        return exams_result

    @cached_property
    def test_state(self) -> int:
        if self.is_complete:
            return self.SEMESTER_TEST_PASSED  # зачёт стоит
        elif self.exercises.count() >= self.required_exercises and \
                        tuple(self.exams_result.values()).count('') == 0:
            return self.SEMESTER_TEST_READY  # может получить зачёт
        else:
            return self.SEMESTER_TEST_NOT_READY  # не может получить зачёт

    class Meta:
        indexes = (
            (('student', 'semester'), True),
        )