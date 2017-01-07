from model.base import BaseModel, ChoiceField
from peewee import CharField


class Group(BaseModel):
    verbose_name = "Группа"
    num = CharField(unique=True, verbose_name='Номер')
    edu_form = ChoiceField(choices=('Очная', 'Заочная'), verbose_name='Форма')

    def __str__(self):
        return self.num
