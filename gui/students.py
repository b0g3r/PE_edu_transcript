from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from gui.helper import get_real_path
from model import Group, Student


class StudentsWidget(QWidget):
    def __init__(self, parent: QWidget, group: Group):
        super().__init__(parent=parent)
        self.students = Student.select().where(Student.group == Group)

        self.init_ui()

    def init_ui(self):
      pass
