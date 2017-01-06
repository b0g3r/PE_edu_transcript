"""Отвечает за главное окно программы
"""
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from gui.helper import get_real_path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(flags=Qt.Window)
        uic.loadUi(get_real_path(r'gui\main_window.ui'), self)

    def init_ui(self):
        """Инициализирует элементы интерфейса
        """
