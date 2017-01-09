"""
Модуль, отвечающий за модели.
Базовая модель описана в `base.py`
Остальные модели в соответствующих файлах
Адаптеры для qt-интерфейса описаны в `adapters.py`
"""

from .base import BaseModel
from .group import Group
from .student import Student
from .exam import Exam, ExamResult
from .exercise import Exercise
from .progress import Progress
from .semester import Semester

