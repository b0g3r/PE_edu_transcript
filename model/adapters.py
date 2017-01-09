from datetime import timedelta

from PyQt5.QtCore import QAbstractTableModel, pyqtSlot
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from peewee import Expression

from model import Group, Student, Exam, ExamResult, BaseModel, Progress, Exercise, Semester
from datetime import date

def daterange(d1: date, d2: date):
    return (d1 + timedelta(days=i) for i in range((d2 - d1).days + 1))


class BasicTableModel(QAbstractTableModel):
    """Необходим для табличного представления peewee-моделей"""

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


class StudentsGeneralDataTableModel(QAbstractTableModel):
    """Выводит краткую информацию о студентах группы"""

    def __init__(self, group: Group, semester: Semester):
        super().__init__()
        self.semester = semester
        self.group = group
        self.refresh_all_data()

    def get_progress(self, student):
        return Progress.get((Progress.student == student) &
                            (Progress.semester == self.semester))

    def refresh_all_data(self):
        self.exams = tuple(self.semester.exams)
        self.progresses = list(self.get_progress(student) for student in self.group.students)  # type: tuple(Progress)
        self.layoutChanged.emit()

    def refresh_row(self, row):
        self.progresses[row] = self.get_progress(tuple(self.group.students)[row])
        self.dataChanged.emit(self.index(row, 0), self.index(row, self.columnCount() - 1))

    def columnCount(self, parent=None, *args, **kwargs):
        column = 1 + 1 + len(self.exams) + 1
        return column

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.progresses)

    def data(self, index: QModelIndex, role=None):
        """Возвращает данные для каждой ячейки"""
        row = index.row()
        column = index.column()
        progress = self.progresses[row]
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if column == 0:
                return str(progress.student)
            elif column == 1:
                return '{}/{}'.format(sum(1 if visit else 0 for visit in progress.visits.values()),
                                      progress.required_exercises)
            elif 1 < column < len(self.exams) + 2:
                return str(progress.exams_result[self.exams[column-2]])

        elif role == Qt.CheckStateRole:
            if column == self.columnCount() - 1:
                return QVariant(Qt.Checked if progress.is_complete else Qt.Unchecked)

        elif role == Qt.BackgroundColorRole:
            if column == 0:
                if progress.test_state == Progress.SEMESTER_TEST_PASSED:
                    return QVariant(QColor(Qt.green))
                elif progress.test_state == Progress.SEMESTER_TEST_READY:
                    return QVariant(QColor(Qt.yellow))

        else:
            return QVariant()

    def headerData(self, column, orientation, role=None):
        """Возвращает заголовок для каждого столбца"""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if column == 0:
                return "ФИО"
            elif column == 1:
                return "Посещений"
            elif 1 < column < len(self.exams) + 2:
                return str(self.exams[column-2])
            elif column == self.columnCount() - 1:
                return "Зачет"
        else:
            return QVariant()

    def flags(self, index: QModelIndex):
        column = index.column()
        if 1 < column < len(self.exams) + 2:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        elif column == self.columnCount() - 1:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        else:
            return Qt.ItemIsEnabled

    def setData(self, index: QModelIndex, value: str, role=None):
        row = index.row()
        column = index.column()
        progress = self.progresses[row]
        if 1 < column < len(self.exams) + 2 and value.isdigit():
            exam_result, created = ExamResult.get_or_create(defaults={'value': value}, exam=self.exams[column - 2],
                                                            progress=progress)
            if not created:
                exam_result.value = value
                exam_result.save()
            self.refresh_row(row)
            return True
        elif column == self.columnCount() - 1:
            if value == 2:
                progress.is_complete = True
            elif value == 0:
                progress.is_complete = False
            else:
                return False
            progress.save()
            self.refresh_row(row)
            return True
        return False

class StudentsFullDataTableModel(QAbstractTableModel):
    """Необходим для табличного представления peewee-моделей"""

    def __init__(self, group: Group, month: date):
        super().__init__()
        self.month = month.replace(day=1)
        self.group = group
        self.number_of_days = self.get_number_of_days(self.month)
        self.semester = Semester.get(Semester.start_date <= self.month <= Semester.end_date)
        self.refresh_all_data()

    def get_progress(self, student):
        return Progress.get((Progress.student == student) &
                            (Progress.semester == self.semester))

    def refresh_all_data(self):
        self.exams = tuple(self.semester.exams)
        self.progresses = list(self.get_progress(student) for student in self.group.students)  # type: tuple(Progress)
        self.layoutChanged.emit()

    def refresh_row(self, row):
        self.progresses[row] = self.get_progress(tuple(self.group.students)[row])
        self.dataChanged.emit(self.index(row, 0), self.index(row, self.columnCount() - 1))

    def get_number_of_days(self, month_date):
        next_month = month_date.replace(day=28) + timedelta(days=4)  # this will never fail
        return (next_month - timedelta(days=next_month.day)).day

    def columnCount(self, parent=None, *args, **kwargs):
        column = 1 + self.number_of_days + len(self.exams) + 1
        return column

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.progresses)

    def data(self, index: QModelIndex, role=None):
        """Возвращает данные для каждой ячейки"""
        row = index.row()
        column = index.column()
        progress = self.progresses[row]
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if column == 0:
                return str(progress.student)
            elif 0 < column < self.number_of_days + 1:
                if progress.visits[self.month.replace(day=column)]:
                    visits_count = 0
                    for day in daterange(self.semester.start_date,
                                         min((self.month.replace(day=column)), self.semester.end_date)):
                        visits_count += progress.visits[day]
                    return str(visits_count)
                else:
                    return ''
            elif self.number_of_days < column < len(self.exams) + self.number_of_days + 1:
                return str(progress.exams_result[self.exams[column - (self.number_of_days + 1)]])

        elif role == Qt.CheckStateRole:
            if column == self.columnCount() - 1:
                return QVariant(Qt.Checked if progress.is_complete else Qt.Unchecked)

        elif role == Qt.BackgroundColorRole:
            if column == 0:
                if progress.test_state == Progress.SEMESTER_TEST_PASSED:
                    return QVariant(QColor(Qt.green))
                elif progress.test_state == Progress.SEMESTER_TEST_READY:
                    return QVariant(QColor(Qt.yellow))
        else:
            return QVariant()

    def setData(self, index: QModelIndex, value: str, role=None):
        row = index.row()
        column = index.column()
        progress = self.progresses[row]
        if self.number_of_days < column < len(self.exams) + self.number_of_days + 1 and value.isdigit():
            exam_result, created = ExamResult.get_or_create(defaults={'value': value}, exam=self.exams[column - (self.number_of_days + 1)],
                                                            progress=progress)
            if not created:
                exam_result.value = value
                exam_result.save()
            self.refresh_row(row)
            return True
        elif column == self.columnCount() - 1:
            if value == 2:
                progress.is_complete = True
            elif value == 0:
                progress.is_complete = False
            else:
                return False
            progress.save()
            self.refresh_row(row)
            return True
        return False


    def flags(self, index: QModelIndex):
        column = index.column()
        if self.number_of_days < column < len(self.exams) + self.number_of_days + 1:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        elif column == self.columnCount() - 1:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        else:
            return Qt.ItemIsEnabled

    def headerData(self, column, orientation, role=None):
        """Возвращает заголовок для каждого столбца"""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if column == 0:
                return "ФИО"
            elif 0 < column < self.number_of_days + 1:
                return column
            elif self.number_of_days < column < len(self.exams) + self.number_of_days + 1:
                return str(self.exams[column - (self.number_of_days + 1)])
            elif column == self.columnCount() - 1:
                return "Зачет"
        else:
            return QVariant()

    @pyqtSlot(QModelIndex, name='clicked')
    def clicked(self, index: QModelIndex):
        row = index.row()
        column = index.column()
        progress = self.progresses[row]
        if 0 < column < self.number_of_days + 1:
            if progress.visits[self.month.replace(day=column)] < 3:
                Exercise.create(progress=progress,
                                date=self.month.replace(day=column))
            else:
                q = Exercise.delete().where((Exercise.progress == progress) &
                                            (Exercise.date == self.month.replace(day=column)))
                q.execute()
            self.refresh_row(row)
