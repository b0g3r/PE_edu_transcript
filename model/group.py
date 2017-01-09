from model.base import BaseModel, ChoiceField
from peewee import CharField, DateField, IntegerField

from datetime import date

class Group(BaseModel):
    verbose_name = "Группа"
    num = CharField(unique=True, verbose_name='Номер')
    edu_form = ChoiceField(choices=('Очная', 'Заочная'), verbose_name='Форма')
    admission_year = IntegerField(verbose_name="Год поступления")

    def __str__(self):
        return self.num
