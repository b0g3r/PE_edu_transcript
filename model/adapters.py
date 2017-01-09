from datetime import timedelta

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QAbstractTableModel, pyqtSlot
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from peewee import Expression

from model import *
from datetime import date

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
    """Необходим для табличного представления peewee-моделей"""

    def __init__(self, group: Group, semester: Semester):
        super().__init__()
        self.semester = semester
        self.group = group
        self.exams = tuple(semester.exams)
        self.students = tuple(self.group.students)
        self.students_data = []
        for student in self.students:
            progress = Progress.get((Progress.student == student) &
                                    (Progress.semester == semester))
            exams_result = {}
            for exam in self.exams:
                try:
                    exams_result[exam] = str(ExamResult.get((ExamResult.exam == exam) &
                                                            (ExamResult.progress == progress)))
                except ExamResult.DoesNotExist:
                    exams_result[exam] = ''
            count_of_exercises = len(tuple(progress.exercises))
            self.students_data.append((progress, exams_result, count_of_exercises))


    def columnCount(self, parent=None, *args, **kwargs):
        column = 1 + 1 + len(self.exams) + 1
        return column

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.students)

    def data(self, index: QModelIndex, role=None):
        """Возвращает данные для каждой ячейки"""
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()

            if column == 0:
                return self.students[row].name
            elif column == 1:
                return '{}/{}'.format(self.students_data[row][2],
                                      self.students_data[row][0].required_exercises)
            elif 1 < column < len(self.exams) + 2:
                return self.students_data[row][1][self.exams[column-2]]
            elif column == self.columnCount() - 1:
                return 'да' if self.students_data[row][0].is_complete else 'нет'
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



def daterange(d1: date, d2: date):
    return (d1 + timedelta(days=i) for i in range((d2 - d1).days + 1))


class StudentsFullDataTableModel(QAbstractTableModel):
    """Необходим для табличного представления peewee-моделей"""

    def __init__(self, group: Group, month: date):
        super().__init__()
        self.month = month.replace(day=1)
        self.group = group
        self.number_of_days = self.get_number_of_days(self.month)
        self.refresh_data()

    def refresh_data(self):
        self.semester = Semester.get(Semester.start_date <= self.month <= Semester.end_date)
        self.count = 0
        self.exams = tuple(self.semester.exams)
        self.students = tuple(self.group.students)
        self.students_data = []
        for student in self.students:
            progress = Progress.get((Progress.student == student) &
                                    (Progress.semester == self.semester))
            exams_result = {}
            for exam in self.exams:
                try:
                    exams_result[exam] = str(ExamResult.get((ExamResult.exam == exam) &
                                                            (ExamResult.progress == progress)))
                except ExamResult.DoesNotExist:
                    exams_result[exam] = ''
            visits = {}
            exercises = tuple(exercise.date for exercise in progress.exercises)

            for day in daterange(self.semester.start_date, self.semester.end_date):
                visits[day] = exercises.count(day)

            self.students_data.append((progress, exams_result, visits))
        self.layoutChanged.emit()

    def refresh_row(self, row):
        student = self.students[row]
        progress = Progress.get((Progress.student == student) &
                                (Progress.semester == self.semester))
        exams_result = {}
        for exam in self.exams:
            try:
                exams_result[exam] = str(ExamResult.get((ExamResult.exam == exam) &
                                                        (ExamResult.progress == progress)))
            except ExamResult.DoesNotExist:
                exams_result[exam] = ''
        visits = {}
        exercises = tuple(exercise.date for exercise in progress.exercises)

        for day in daterange(self.semester.start_date, self.semester.end_date):
            visits[day] = exercises.count(day)

        self.students_data[row] = (progress, exams_result, visits)
        self.dataChanged.emit(self.index(row, 0), self.index(row, self.columnCount()-1))

    def get_number_of_days(self, month_date):
        next_month = month_date.replace(day=28) + timedelta(days=4)  # this will never fail
        return (next_month - timedelta(days=next_month.day)).day

    def columnCount(self, parent=None, *args, **kwargs):
        column = 1 + self.number_of_days + len(self.exams) + 1
        return column

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.students)

    def data(self, index: QModelIndex, role=None):
        """Возвращает данные для каждой ячейки"""
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            if column == 0:
                return str(self.students[row])
            elif 0 < column < self.number_of_days + 1:
                if self.students_data[row][2][self.month.replace(day=column)]:
                    visits_count = 0
                    for day in daterange(self.semester.start_date, self.month.replace(day=column)):
                        visits_count += self.students_data[row][2][day]
                    return str(visits_count)
                else:
                    return ''
            elif self.number_of_days < column < len(self.exams) + self.number_of_days + 1:
                return self.students_data[row][1][self.exams[column - (self.number_of_days + 1)]]
            elif column == self.columnCount() - 1:
                return 'да' if self.students_data[row][0].is_complete else 'нет'
        else:
            return QVariant()

    def setData(self, index: QModelIndex, value, role=None):
        row = index.row()
        column = index.column()
        print(value)
        if self.number_of_days < column < len(self.exams) + self.number_of_days + 1 and value:
            exam_result, _ = ExamResult.get_or_create(exam=self.exams[column - (self.number_of_days + 1)],
                                                      progress=self.students_data[row][0])
            exam_result.value = value
            exam_result.save()
            self.refresh_row(row)
            return True
        return False

    def flags(self, index: QModelIndex):

        column = index.column()
        if self.number_of_days < column < len(self.exams) + self.number_of_days + 1:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled
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

        if 0 < column < self.number_of_days + 1:
            if self.students_data[row][2][self.month.replace(day=column)] < 3:
                Exercise.create(progress=self.students_data[row][0], date=self.month.replace(day=column))
            else:
                q = Exercise.delete().where((Exercise.progress == self.students_data[row][0]) &
                                            (Exercise.date == self.month.replace(day=column)))
                q.execute()
            self.refresh_row(row)
