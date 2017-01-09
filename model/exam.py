from peewee import CharField, ForeignKeyField, FloatField

from .base import BaseModel
from .semester import Semester
from .progress import Progress


class Exam(BaseModel):
    name = CharField()  # type: str
    semester = ForeignKeyField(Semester, related_name='exams')  # type: Semester

    def __str__(self):
        return self.name


class ExamResult(BaseModel):
    exam = ForeignKeyField(Exam)  #type: Exam
    progress = ForeignKeyField(Progress)  #type: Progress
    value = FloatField(null=True)  #type: float

    def __str__(self):
        return str(self.value)

    class Meta:
        indexes = (
            (('exam', 'progress'), True),
        )