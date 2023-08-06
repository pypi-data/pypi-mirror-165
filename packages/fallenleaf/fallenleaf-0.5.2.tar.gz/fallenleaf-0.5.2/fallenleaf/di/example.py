# just put this code into your main file
from fallenleaf.di import Container, Singleton, Factory, DeclarativeContainer, Provide


class Human:
    pass


class Teacher:
    pass


class Student:
    def __init__(self, teacher: Teacher|Human):
        self.teacher = teacher


def build_student(container, blueprint, teacher: Teacher):
    return blueprint(teacher)


school = Container()
school.bind(Singleton(Teacher))
school.bind(Factory(Student, build_student))

student1 = school.make(Student)
student2 = school.make(Student)

assert student1 != student2
assert student1.teacher == student2.teacher


class School(DeclarativeContainer):
    teacher = Provide(Teacher, Singleton)
    student = Provide(Student, Factory)

myschool = School()

student1 = myschool.make(Student)
student2 = myschool.make(Student)

assert student1 != student2
assert  student1.teacher == student2.teacher