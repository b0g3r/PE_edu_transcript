from peewee import CharField, ForeignKeyField, FloatField, IntegerField

from .base import BaseModel
from .semester import Semester
from .progress import Progress


class Exam(BaseModel):
    name = CharField()  # type: str
    semester = ForeignKeyField(Semester, related_name='exams')  # type: Semester

    def get_result_for_progress(self, progress: Progress):
        try:
            return str(self.results.where(ExamResult.progress == progress).get())
        except ExamResult.DoesNotExist:
            return ''

    def __str__(self):
        return self.name


class ExamResult(BaseModel):
    exam = ForeignKeyField(Exam, related_name='results')  # type: Exam
    progress = ForeignKeyField(Progress)  # type: Progress
    value = IntegerField(null=True)  # type: float

    def __str__(self):
        return str(self.value)

    class Meta:
        indexes = (
            (('exam', 'progress'), True),
        )