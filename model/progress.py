from datetime import date

from peewee import ForeignKeyField, IntegerField, BooleanField

from .base import BaseModel
from .student import Student
from .semester import  Semester


class Progress(BaseModel):
    student = ForeignKeyField(Student)  # type: Student
    semester = ForeignKeyField(Semester)  # type: Semester
    required_exercises = IntegerField()  # type: int
    is_complete = BooleanField(default=False)  # type: bool

    def save(self, *args, **kwargs):
        self.required_exercises = self.get_default_count_of_exercises()
        return super().save(*args, **kwargs)


    def get_default_count_of_exercises(self):
        course_number = (self.semester.start_date - date(self.student.group.admission_year, 9, 1)).days//365 + 1
        if course_number == 1:
            return 14
        elif course_number == 2:
            return 12
        elif course_number == 3:
            return 10
        elif course_number == 4:
            return 8

    class Meta:
        indexes = (
            (('student', 'semester'), True),
        )