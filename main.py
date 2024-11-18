class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        avg_grade = self.average_grade()
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {avg_grade:.1f}"

    def average_grade(self):
        if not self.grades:
            return 0
        all_grades = [grade for grades_list in self.grades.values() for grade in grades_list]
        return sum(all_grades) / len(all_grades)

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() < other.average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return super().__str__()


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        avg_grade = self.average_grade()
        courses_in_progress = ", ".join(self.courses_in_progress)
        finished_courses = ", ".join(self.finished_courses)
        return (f"Имя: {self.name}\nФамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {avg_grade:.1f}\n"
                f"Курсы в процессе изучения: {courses_in_progress}\n"
                f"Завершенные курсы: {finished_courses}")

    def average_grade(self):
        if not self.grades:
            return 0
        all_grades = [grade for grades_list in self.grades.values() for grade in grades_list]
        return sum(all_grades) / len(all_grades)

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() < other.average_grade()


# Функции подсчета средней оценки
def average_student_grade(students, course):
    all_grades = []
    for student in students:
        if course in student.grades:
            all_grades.extend(student.grades[course])
    if not all_grades:
        return 0
    return sum(all_grades) / len(all_grades)


def average_lecturer_grade(lecturers, course):
    all_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            all_grades.extend(lecturer.grades[course])
    if not all_grades:
        return 0
    return sum(all_grades) / len(all_grades)


# Пример использования:

# Создаем студентов
student1 = Student('Иван', 'Абрамов', 'male')
student1.courses_in_progress += ['Python', 'Git']
student1.finished_courses += ['Введение в программирование']

student2 = Student('Зоя', 'Солдана', 'female')
student2.courses_in_progress += ['Python']

# Создаем преподавателей
lecturer1 = Lecturer('Павел', 'Прилучный')
lecturer1.courses_attached += ['Python']

lecturer2 = Lecturer('Катя', 'Ко')
lecturer2.courses_attached += ['Git']

# Создаем проверяющих
reviewer1 = Reviewer('Пол', 'Атрейдас')
reviewer1.courses_attached += ['Python']

reviewer2 = Reviewer('Майкл', 'Джексон')
reviewer2.courses_attached += ['Git']

# Выставляем оценки студентам
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student2, 'Python', 8)

# Студенты оценивают лекторов
student1.rate_lecturer(lecturer1, 'Python', 10)
student1.rate_lecturer(lecturer1, 'Python', 9)
student1.rate_lecturer(lecturer2, 'Git', 8)

student2.rate_lecturer(lecturer1, 'Python', 7)

# Вывод объектов
print(student1)
print()
print(student2)
print()
print(lecturer1)
print()
print(lecturer2)
print()
print(reviewer1)
print()
print(reviewer2)

# Подсчет средних оценок
students = [student1, student2]
lecturers = [lecturer1, lecturer2]

print(f"Средняя оценка за домашние задания по Python: {average_student_grade(students, 'Python'):.1f}")
print(f"Средняя оценка за лекции по Python: {average_lecturer_grade(lecturers, 'Python'):.1f}")
