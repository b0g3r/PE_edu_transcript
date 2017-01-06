from model import *
group = Group(num='446')
group.save()
student = Student.create(name='Богер', group=group)
