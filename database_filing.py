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

    for i in range(15):
        Discipline.objects.create(
            name = random.choice(discipline_names),
            exam = random.choice(Discipline.EXAM_CHOISES)[0]
        )
        
    for i in range(15):
        Speciality.objects.create(
            name = random.choice(specialities)
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
            speciality = random.choice(Speciality.objects.all())
        )
        
    for i in range(15):
        Teachers.objects.create(
            name = fake.name(),
            study_discipline = random.choice(Discipline.objects.all())
        )
        
            
    for i in range(100):
        group = random.choice(Group.objects.all())
        student = Student.objects.create(
            name = fake.name(),
            group = group,
            speciality = group.speciality,
            study_year = random.randint(2000, 2025),
            is_studying = False,
            is_gradueted = random.choice([True, False]),
            is_expelled = random.choice([True, False])
        )
        if Student.objects.filter(study_year__icontains='2024').exists():
            student.is_studying = True
            student.is_studying = False
            student.is_gradueted = False
