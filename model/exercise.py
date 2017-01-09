from peewee import ForeignKeyField, DateField

from .base import BaseModel
from .progress import Progress


class Exercise(BaseModel):
    progress = ForeignKeyField(Progress, related_name='exercises')  # type: Progress
    date = DateField()  # type: date

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')