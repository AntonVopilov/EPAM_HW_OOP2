import datetime
from datetime import datetime, timedelta
from collections import defaultdict


class HomeWorkError(Exception):
    """Exceptions in HomeWork functions"""
    pass


class DeadlineError(HomeWorkError):
    """Deadline lost in the past..."""

    def __init__(self, message):
        self.message = message


class Homework:

    def __init__(self, text, deadline_days=14):
        self.text = text
        self.created = datetime.today()
        self.deadline = timedelta(days=deadline_days, hours=0, seconds=0)

    def is_active(self):
        return self.created + self.deadline > datetime.today()


class HomeworkResult:
    """
    HomeworkResult принимает объект автора задания, принимает исходное задание
    и его решение в виде строки
    Атрибуты:
    homework - для объекта Homework, если передан не этот класс -  выкинуть
    подходящие по смыслу исключение с сообщением:
    'You gave a not Homework object'
    solution - хранит решение ДЗ как строку
    author - хранит объект Student
    created - c точной датой и временем создания
    """

    def __init__(self, author, home_task: Homework, solution):

        if isinstance(author, Student):
            self.author = author
        else:
            raise TypeError('You gave a not Student object')

        if isinstance(home_task, Homework):
            self.homework = home_task
        else:
            raise TypeError('You gave a not Homework object')

        self.author = author
        self.created = home_task.created
        self.solution = str(solution)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.author == other.author and \
                   self.solution == other.solution and \
                   self.homework == other.homework

    def __hash__(self):
        return id(self)


class Somebody:
    """
    Student и Teacher имеют одинаковые по смыслу атрибуты
    (last_name, first_name) - избавиться от дублирования с помощью наследования
    """

    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.last_name == other.last_name and \
                   self.first_name == other.first_name


class Student(Somebody):
    """
    Как то не правильно, что после do_homework мы возвращаем все тот же
    объект - будем возвращать какой-то результат работы (HomeworkResult)
    Если задание уже просрочено хотелось бы видеть исключение при do_homework,
    а не просто принт 'You are late'.
    Поднимайте исключение DeadlineError с сообщением 'You are late' вместо print.
    """

    def do_homework(self, hw: Homework, solution):

        if hw.is_active():
            return HomeworkResult(self, hw, solution)
        else:
            raise DeadlineError('You are late')


class Teacher(Somebody):
    """
    Teacher
    Атрибут:
        homework_done - структура с интерфейсом как в словаря, сюда поподают все
        HomeworkResult после успешного прохождения check_homework
        (нужно гаранитровать остутствие повторяющихся результатов по каждому
        заданию), группировать по экземплярам Homework.
        Общий для всех учителей. Вариант ипользования смотри в блоке if __main__...
    Методы:
        check_homework - принимает экземпляр HomeworkResult и возвращает True если
        ответ студента больше 5 символов, так же при успешной проверке добавить в
        homework_done.
        Если меньше 5 символов - никуда не добавлять и вернуть False.
        reset_results - если передать экземпряр Homework - удаляет только
        результаты этого задания из homework_done, если ничего не передавать,
        то полностью обнулит homework_done.
    """

    homework_done = defaultdict()

    def check_homework(self, homework_result_obj: HomeworkResult):

        if len(homework_result_obj.solution) > 5:

            if homework_result_obj.homework in self.homework_done:
                print('You try to add existing homework result')
            else:
                self.homework_done[homework_result_obj.homework] = homework_result_obj
                return True

            return False

    @classmethod
    def reset_results(cls, homework_obj=None):
        if not homework_obj:
            cls.homework_done = cls.homework_done.clear()
        elif homework_obj in cls.homework_done:
            cls.homework_done.pop(homework_obj)

    @staticmethod
    def create_homework(text, deadline_days):
        return Homework(text, deadline_days)


if __name__ == '__main__':
    opp_teacher = Teacher('Daniil', 'Shadrin')
    advanced_python_teacher = Teacher('Aleksandr', 'Smetanin')

    lazy_student = Student('Roman', 'Petrov')
    good_student = Student('Lev', 'Sokolov')

    oop_hw = opp_teacher.create_homework('Learn OOP', 1)
    docs_hw = opp_teacher.create_homework('Read docs', 5)

    result_1 = good_student.do_homework(oop_hw, 'I have done this hw')
    result_2 = good_student.do_homework(docs_hw, 'I have done this hw too')
    result_3 = lazy_student.do_homework(docs_hw, 'done any chars for to go under condition')

    try:
        result_4 = HomeworkResult(good_student, "fff", "Solution")
    except Exception as err:
        print(err)
        print('There was an exception here')

    opp_teacher.check_homework(result_1)
    temp_1 = opp_teacher.homework_done

    advanced_python_teacher.check_homework(result_1)
    temp_2 = Teacher.homework_done

    assert temp_1 == temp_2

    opp_teacher.check_homework(result_2)
    opp_teacher.check_homework(result_3)

    print(Teacher.homework_done[oop_hw])

    Teacher.reset_results()
    print(Teacher.homework_done)
