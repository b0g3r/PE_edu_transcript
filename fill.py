import sys

from PyQt5.QtWidgets import QPushButton

from model import create_db
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from model import Group, Student, Exam, ExamResult, Exercise, Progress, Semester
from datetime import date
from dateutil.relativedelta import relativedelta

g446 = Group.create(num='446', edu_form='Очная', admission_year=2014)
boger = Student.create(name='Богер Дмитрий Александович', group=g446)
sokol = Student.create(name='Соколовская Татьяна Сергеевна', group=g446)

first_sem = Semester.create(start_date=date(2016, 9, 1), end_date=date(2017, 1, 29))

first_exam = Exam.create(name='Отжимания', semester=first_sem)
second_exam = Exam.create(name='Пресс', semester=first_sem)

progress = Progress.create(student=boger, semester=first_sem)
second_progress = Progress.create(student=sokol, semester=first_sem)

Exercise.create(progress=progress, date=date(2016, 9, 1))
Exercise.create(progress=progress, date=date(2016, 9, 20))
Exercise.create(progress=progress, date=date(2016, 9, 2))
Exercise.create(progress=progress, date=date(2016, 9, 2))
Exercise.create(progress=progress, date=date(2016, 9, 19))

Exercise.create(progress=progress, date=date(2016, 10, 19))

ExamResult.create(exam=first_exam, progress=progress, value=50)
ExamResult.create(exam=second_exam, progress=progress, value=50)
ExamResult.create(exam=second_exam, progress=second_progress, value=100)


"""Отвечает за главное окно программы
"""
from PyQt5.QtWidgets import QMainWindow

from model.adapters import *

class MainWindow(QMainWindow):
    """Главное окно программы"""
    def __init__(self):
        super().__init__(flags=Qt.Window)
        self.init_ui()

    def init_ui(self):
        """Инициализирует элементы интерфейса
        """
        self.month = date(2016,9,1)

        self.setCentralWidget(QtWidgets.QWidget())
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget())

        #self.model = StudentsGeneralDataTableModel(Group.get(), Semester.get())
        self.tableView = QtWidgets.QTableView()

        self.horizontalLayout.addWidget(self.tableView)
        self.button = QPushButton()
        self.button.clicked.connect(self.aaa)
        self.horizontalLayout.addWidget(self.button)
        self.show()

    def aaa(self):
        self.month += relativedelta(months=1)
        self.model = StudentsFullDataTableModel(Group.get(), self.month)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        self.tableView.clicked.connect(self.model.clicked)

app = QApplication(sys.argv)

ex = MainWindow()
sys.exit(app.exec_())