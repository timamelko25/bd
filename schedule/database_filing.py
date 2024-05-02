from schedule.models import *
import random
from faker import Faker
fake = Faker('ru_RU')
class Data():
    def main(self):
        discipline_names = [
                "Математика",
                "Физика",
                "Информатика",
                "Химия",
                "Биология",
                "История",
                "Литература",
                "Иностранный язык",
                "Философия",
                "Экономика",
                "Политология",
                "География",
                "Психология",
                "Социология",
                "Юриспруденция"
            ]

        specialities = [
                "Программная инженерия",
                "Медицина",
                "Экономика",
                "Психология",
                "Автоматизация технологических процессов",
                "Лингвистика",
                "Химическая технология",
                "Бухгалтерский учет и аудит",
                "Маркетинг",
                "Гражданская защита",
                "Авиационная и ракетно-космическая техника",
                "Архитектура",
                'Технология оборудования и электроинструмент',
                "Информационная безопасность",
                "Компьютерная безопасность"
                ]

        for i in range(15):
            Discipline.objects.create(
                name = discipline_names[i],
                exam = random.choice(Discipline.EXAM_CHOISES)[0]
            )
            
        for i in range(15):
            Speciality.objects.create(
                name=specialities[i]
            )
            
        for i in range(60):
            SpecialityDiscipline.objects.create(
                speciality = random.choice(Speciality.objects.all()),
                discipline = random.choice(Discipline.objects.all()),
                duration_discipline = random.choice(SpecialityDiscipline.DURATION_CHOICES)[0],
                semester_discipline = random.choice(SpecialityDiscipline.SEMESTER_CHOICES)[0]
            )
            
        for i in range(15):
            Group.objects.create(
                group_number = i+1,
                speciality = Speciality.objects.get(id=i+1)
            )
            
        for i in range(15):
            Teachers.objects.create(
                name = fake.name(),
                study_discipline = random.choice(Discipline.objects.all())
            )
            
                
        for i in range(1000):
            group = random.choice(Group.objects.all())
            student = Student.objects.create(
                name = fake.name(),
                group = group,
                speciality = group.speciality,
                study_year = random.randint(2000, 2024),
                is_studying = False,
                is_gradueted = random.choice([True, False]),
                is_expelled = random.choice([True, False])
            )
            if Student.objects.filter(study_year='2024').exists():
                student.is_studying = True
                student.is_studying = False
                student.is_gradueted = False

        for i in range(100):
            Session.objects.create(
                semestr = random.choice([1,2]),
                year = random.randint(2000, 2024),
                student = random.choice(Student.objects.all()),
                teacher = random.choice(Teachers.objects.all()),
                discipline = random.choice(Discipline.objects.all()),
                mark = random.choice(Session.MARK_CHOICES)[0]
            )
            
        for i in range(100):
            group = random.choice(Group.objects.all())
            Schedule.objects.create(
                date = fake.date_between(start_date='-24y', end_date='now'),
                semester = random.choice([1,2]),
                group = group,
                discipline = random.choice(Discipline.objects.all()),
                teacher = random.choice(Teachers.objects.all())
            )
