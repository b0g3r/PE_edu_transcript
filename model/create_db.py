from model.student import Student
from model.group import Group
from model.base import db

if __name__ == '__main__':
    db.connect()
    db.drop_tables([Student, Group])
    db.create_tables([Student, Group])