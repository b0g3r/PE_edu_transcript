"""Отвечает за главное окно программы
"""
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from gui.helper import get_real_path
from model import *


class MainWindow(QMainWindow):
    """Главное окно программы"""
    def __init__(self):
        super().__init__(flags=Qt.Window)
        uic.loadUi(get_real_path(r'gui\main_window.ui'), self)
        self.init_ui()

    def init_ui(self):
        """Инициализирует элементы интерфейса
        """
        model = PeeweeTableModel(Student, order=Student.name)
        self.tableView.setModel(model)
        self.listView.setModel(model)
        self.treeView.setModel(model)
        self.columnView.setModel(model)
        self.show()
