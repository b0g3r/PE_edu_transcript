from peewee import CharField, ForeignKeyField

from model.base import BaseModel
from model.group import Group


class Student(BaseModel):
    verbose_name = "Студент"
    name = CharField(verbose_name='ФИО')
    group = ForeignKeyField(Group, related_name='students', verbose_name='Группа')

    def __str__(self):
        return self.name
