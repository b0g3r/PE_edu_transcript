from peewee import CharField, ForeignKeyField

from model.base import BaseModel
from model.group import Group


class Student(BaseModel):
    verbose_name = "Студент"
    name = CharField(verbose_name='ФИО')  # type: str
    group = ForeignKeyField(Group, related_name='students', verbose_name='Группа')  # type: Group

    def __str__(self):
        return '{0[0]} {0[1][0]}.'.format(self.name.split())
