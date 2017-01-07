from peewee import SqliteDatabase, Model, IntegerField

db = SqliteDatabase('test.db')


class BaseModel(Model):

    @property
    def verbose_name(self):
        raise NotImplementedError()

    def __repr__(self):
        return '<model.{} object ({}) at {}>'.format(
            self.__class__.__name__,
            ', '.join('{}: {!r}'.format(key, self.__getattribute__(key)) for key in self._meta.fields),
            hex(id(self)).upper())

    class Meta:
        database = db


class ChoiceField(IntegerField):
    def db_value(self, value):
        return self.choices.index(value)

    def python_value(self, value):
        return self.choices[value]

