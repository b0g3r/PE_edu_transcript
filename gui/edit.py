from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from peewee import IntegrityError, CharField, ForeignKeyField

from model.base import BaseModel, ChoiceField


class EditDialog(QDialog):
    def __init__(self, model: BaseModel):
        super().__init__()
        self.choices = {}
        self.bind = {}
        self.model = model
        self.formLayout = QFormLayout(self)
        self.formLayout.setObjectName("formLayout")
        self.setWindowTitle(self.model.verbose_name)
        for i, model_field in enumerate(self.model._meta.sorted_fields[1:]):  # without primary-key field (`id`)
            label = QLabel(self)
            label.setText(model_field.verbose_name)
            if isinstance(model_field, CharField):
                field = QLineEdit(self)
            elif isinstance(model_field, ChoiceField):
                field = QComboBox(self)
                field.addItems(model_field.choices)
            elif isinstance(model_field, ForeignKeyField):
                field = QComboBox(self)
                choice = {str(group): group.get_id() for group in model_field.rel_model.select()}
                self.choices[model_field] = choice
                field.addItems(choice.keys())
            else:
                raise Exception('Попытка сгенерировать интерфейс не удалась - не умею такое поле')
            self.formLayout.setWidget(i, QFormLayout.LabelRole, label)
            self.formLayout.setWidget(i, QFormLayout.FieldRole, field)
            self.bind[model_field] = field
        else:
            self.button = QPushButton(self)
            self.formLayout.setWidget(i+1, QFormLayout.SpanningRole, self.button)

        self.init_ui()

    def init_ui(self):
        """Инициилизурет элементы интерфейса перед показом"""
        if isinstance(self.model, type):
            self.button.setText('Добавить')
            self.button.clicked.connect(self.add)
        else:
            self.button.setText('Изменить')
            self.button.clicked.connect(self.edit)
            for model_field, qt_field in self.bind.items():
                name = model_field.name
                value = getattr(self.model, name)
                if isinstance(model_field, CharField):
                    qt_field.setText(value)
                elif isinstance(model_field, ChoiceField):
                    qt_field.setCurrentIndex(model_field.choices.index(value))
                elif isinstance(model_field, ForeignKeyField):
                    qt_field.setCurrentText(str(value))
                else:
                    raise Exception('Попытка сгенерировать интерфейс не удалась - не умею такое поле')

    def edit(self):
        """Изменяет инстанс модели"""
        self.save(self.model)

    def add(self):
        """Добавляет новый инстанс модели"""
        model = self.model()
        self.save(model)

    def save(self, model: BaseModel):
        for model_field, qt_field in self.bind.items():
            name = model_field.name
            if isinstance(model_field, CharField):
                setattr(model, name, qt_field.text())
            elif isinstance(model_field, ChoiceField):
                setattr(model, name, qt_field.currentText())
            elif isinstance(model_field, ForeignKeyField):
                setattr(model, name, self.choices[model_field][qt_field.currentText()])
            else:
                raise Exception('Попытка не удалась - не умею такое поле')
        try:
            model.save()
        except IntegrityError:  # peewee.IntegrityError: UNIQUE constraint failed: group.num
            pass  # TODO: вывод ошибки о уже существующей группе
        else:
            self.accept()
