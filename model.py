from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt
from peewee import *
db = SqliteDatabase('test.db')


class Group(Model):
    num = CharField()

    def __repr__(self):
        return '<model.{} object ({}) at {}>'.format(
            self.__class__.__name__,
            ', '.join('{}: {}'.format(key, self.__getattribute__(key)) for key in self._meta.fields),
            hex(id(self))).upper()

    class Meta:
        database = db


class Student(Model):
    name = CharField()
    group = ForeignKeyField(Group, related_name='students')

    def __repr__(self):
        return '<model.{} object ({}) at {}>'.format(
            self.__class__.__name__,
            ', '.join('{}: {}'.format(key, self.__getattribute__(key)) for key in self._meta.fields),
            hex(id(self))).upper()

    class Meta:
        database = db


class PeeweeTableModel(QAbstractTableModel):
    """Необходим для табличного представления моделей"""

    def __init__(self, model, query=None):
        super().__init__()
        self.model = model
        self.query = query

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.model._meta.fields)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.model.select(self.query).count())

    def data(self, index: QModelIndex, role=None):
        if not index.isValid():
            return tuple()
        elif role == Qt.DisplayRole:
            index.row()
