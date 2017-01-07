"""Отвечает за главное окно программы
"""
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from gui.helper import get_real_path
from model.adapters import PeeweeTableModel
from model.student import Student
from model.group import Group


class MainWindow(QMainWindow):
    """Главное окно программы"""
    def __init__(self):
        super().__init__(flags=Qt.Window)
        uic.loadUi(get_real_path(r'gui\main_window.ui'), self)
        self.init_ui()

    def init_ui(self):
        """Инициализирует элементы интерфейса
        """
        from gui.edit import EditDialog
        EditDialog(Student.get()).exec_()
        model = PeeweeTableModel(Group, order=+Group.num)
        model2 = PeeweeTableModel(Student, order=+Student.name)
        self.tableView.setModel(model)
        self.tableView_2.setModel(model2)
        self.show()
