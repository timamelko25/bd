from schedule.models import *
import random
from faker import Faker
fake = Faker('ru_RU')

class Data():
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
            "Гражданская защита"
        ]

    for _ in range(15):
            name = random.choice(discipline_names)
            
            Discipline.objects.create(
                name=name,
                exam=random.choice(["зачет", "экзамен"])
            )
            
    for i in range(10):
        group_number = i + 1
        if not Group.objects.filter(group_number=group_number).exists():
            Group.objects.create(group_number=group_number)
        
    for i in range(50):
        Student.objects.create(
            name=fake.name(),
            group = random.choice(Group.objects.all()),
            study_year = random.choice(["2001", "2002", "2003", "2004"]),
            
        )
        
    for i in range(10):
        Teachers.objects.create(
            name=fake.name(),
            study_discipline = random.choice(Discipline.objects.all())
        )
        
    for i in range(10):
        Speciality.objects.create(
            name = random.choice(specialities),
            dicicplines = random.choice(Discipline.objects.all()),
            duration_dicipline = random.choice(["1", "2"]),
            semestr_dicipline = random.choice(["1", "2", "1,2"])
        )
        
    for i in range(10):
        Schedule.objects.create(
            data = fake.date_this_year(),
            group = random.choice(Group.objects.all()),
            teacher = random.choice(Teachers.objects.all()),
            discipline = random.choice(Discipline.objects.all()),
            semester = random.choice(["1", "2"])
        )
