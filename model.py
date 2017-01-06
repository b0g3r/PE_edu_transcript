from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from peewee import SqliteDatabase, Model, Expression
from peewee import CharField, ForeignKeyField
db = SqliteDatabase('test.db')

class BaseModel(Model):
    def __repr__(self):
        return '<model.{} object ({}) at {}>'.format(
            self.__class__.__name__,
            ', '.join('{}: {!r}'.format(key, self.__getattribute__(key)) for key in self._meta.fields),
            hex(id(self)).upper())

    class Meta:
        database = db


class Group(BaseModel):
    num = CharField()

    def __str__(self):
        return self.num


class Student(BaseModel):
    name = CharField()
    group = ForeignKeyField(Group, related_name='students')

    def __str__(self):
        return self.name


class PeeweeTableModel(QAbstractTableModel):
    """Необходим для табличного представления моделей"""

    def __init__(self, model: BaseModel, query: Expression = None, order: Expression = None, show_id: bool = False):
        super().__init__()
        self.model = model
        self.query = query
        self.show_id = show_id
        self.entrys = self.model.select().where(self.query).order_by(order)

    def columnCount(self, parent=None, *args, **kwargs):
        column = len(self.model._meta.fields) - 1 if not self.show_id else 0
        return column

    def rowCount(self, parent=None, *args, **kwargs):
        return self.entrys.count()

    def data(self, index: QModelIndex, role=None):
        """Возвращает данные для каждой ячейки"""
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column() + int(not self.show_id)
            return str(self.entrys[row].__getattribute__(self.model._meta.sorted_field_names[column]))
        else:
            return QVariant()

    def headerData(self, column, orientation, role=None):
        """Возвращает заголовок для каждого столбца"""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.model._meta.sorted_field_names[int(not self.show_id) + column]
        else:
            return QVariant()


