from model import *
from model import Semester, Progress, Exam
from model.base import db
from model.exam import ExamResult
from model.exercise import Exercise

db.connect()

db.drop_tables([Student, Group, Semester, Progress, Exercise, Exam, ExamResult])
db.create_tables([Student, Group, Semester, Progress, Exercise, Exam, ExamResult])