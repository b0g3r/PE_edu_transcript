from peewee import DateField

from model import BaseModel


class Semester(BaseModel):
    start_date = DateField()  # type: date
    end_date = DateField()   # type: date