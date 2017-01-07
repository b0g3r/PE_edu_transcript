from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from peewee import Expression

from model.base import BaseModel


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
            return self.model._meta.sorted_fields[int(not self.show_id) + column].verbose_name
        else:
            return QVariant()


