from PyQt5 import uic
from PyQt5.QtCore import QRect
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
from model import Group
from gui.students import StudentsWidget


class GroupsWidget(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)
        self.init_ui()

    def init_ui(self):
        self.verticalLayout = QVBoxLayout(self)
        self.title = QLabel(self)
        font = QFont()
        font.setPointSize(12)
        self.title.setFont(font)
        self.title.setText('Группы:')
        self.verticalLayout.addWidget(self.title)
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.verticalLayout_scroll = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_scroll.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.fill_groups_list()

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

    def fill_groups_list(self):
        for group in Group.select().order_by(+Group.num):
            label = GroupLabel(self, group)
            self.verticalLayout_scroll.addWidget(label)



    def open_students_by_group(self, group):
        """Открывает окно группы"""
        self.parent().set_new_screen(StudentsWidget, group=group)


class GroupLabel(QLabel):

    def __init__(self, parent: GroupsWidget, group: Group):
        super().__init__(parent)
        self.parent = parent
        self.model = group
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum))
        self.setMinimumSize(QSize(0, 30))
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.setIndent(5)
        self.setFrameShape(QFrame.StyledPanel)
        self.setText(str(self.model))
        self.click_on_group = pyqtSignal()

    def mousePressEvent(self, event):
        self.parent.open_students_by_group(self.model)
