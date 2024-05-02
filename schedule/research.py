import sqlite3
import time
import random

from django.shortcuts import get_object_or_404 
from schedule.models import Group, Student, Speciality
from django.db.models import Q
from faker import Faker
fake = Faker('ru_RU')

class Research():
    
    def __init__(self):
        self.avg1 = 0
        self.avg2 = 0
        self.avg3 = 0
        self.avg4 = 0
        self.avg5 = 0
        self.avg6 = 0
        self.avg7 = 0
        self.avg8 = 0
        self.avg9 = 0
        self.avg10 = 0
        self.avg11 = 0
        self.avg12 = 0
        
    def rnd_part(self, name):
        random_speciality = random.choice(name)
        random_length = random.randint(1, len(random_speciality))
        random_start_index = random.randint(0, len(random_speciality) - random_length)
        random_part = random_speciality[random_start_index:random_start_index + random_length]
        return random_part
    
    def search_key(self, choice):
        start_time = time.time()

        Student.objects.filter(id = choice)

        end_time = time.time()
        return end_time - start_time

    def search_not_key(self, choice):
        speciality = Speciality.objects.filter(name=choice)
        start_time = time.time()

        Student.objects.filter(speciality = speciality)

        end_time = time.time()
        return end_time - start_time

    def search_mask(self, choice):
        start_time = time.time()

        Student.objects.filter(speciality__name__icontains=choice)

        end_time = time.time()
        return end_time - start_time

    def add(self):
        group = random.choice(Group.objects.all())
        start_time = time.time()
        Student.objects.create(
            name = fake.name(),
            group = group,
            speciality = group.speciality,
            study_year = 2024
        )
        end_time = time.time()
        return end_time - start_time

    def add_many(self):
        group = random.choice(Group.objects.all())
        start_time = time.time()
        for _ in range(5):
            Student.objects.create(
               name = fake.name(),
               group = group,
               speciality = group.speciality,
               study_year = 2024     
            )
        end_time = time.time()
        return end_time - start_time

    def change(self, choice):
        start_time = time.time()
        Student.objects.filter(id = choice).update(
            name = fake.name(),
        )
        end_time = time.time()
        return end_time - start_time

    def change_many(self, choice1, choice2):
        speciality1 = Speciality.objects.filter(name=choice1).first()
        speciality2 = Speciality.objects.filter(name=choice2).first()
        start_time = time.time()
        tmp1 = Student.objects.filter(speciality=speciality1).first()
        tmp2 = Student.objects.filter(speciality=speciality2).first()

        if tmp1 and tmp2:
            tmp1.name = fake.name()
            tmp2.name = fake.name()
        
            Student.objects.bulk_update([tmp1, tmp2], ["name", "name"])

        end_time = time.time()
        return end_time - start_time

    def delete_key(self, choice):
        start_time = time.time()
        student = Student.objects.filter(id=choice)
        student.delete()
        end_time = time.time()
        return end_time - start_time
    
    def delete_not_key(self, choice):
        start_time = time.time()
        student = Student.objects.filter(name = choice)
        student.delete()
        end_time = time.time()
        return end_time - start_time

    def delete_many(self, choice):
        start_time = time.time()
        student = Student.objects.filter(name = choice)
        student.delete()
        end_time = time.time()
        return end_time - start_time

    def compression1(self, db_name, limit = 200):
        start_time = time.time()
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute('VACUUM')
        connection.close()
        end_time = time.time()
        return end_time - start_time


    def compression2(self, db_name):
        start_time = time.time()
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE temp_table AS SELECT * FROM schedule_student LIMIT 200")
        cursor.execute("DROP TABLE schedule_student")
        cursor.execute("ALTER TABLE temp_table RENAME TO schedule_student")
        cursor.execute("VACUUM")
        connection.close()
        end_time = time.time()
        return end_time-start_time
    
    def random_part(self, choice):
        random_speciality = random.choice(choice)
        random_length = random.randint(1, len(random_speciality))
        random_start_index = random.randint(0, len(random_speciality) - random_length)
        random_part = random_speciality[random_start_index:random_start_index + random_length]
        return random_part
        

    def main(self):
        t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12 = 0,0,0,0,0,0,0,0,0,0,0,0
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
        
        num_experiments = 100
        db = 100000
        db_name = '100000.sqlite3'
        for _ in range(num_experiments):
            t1 += self.search_key(choice = random.randint(1, db))
            t2 += self.search_not_key(choice = random.choice(specialities))
            t3 += self.search_mask(self.rnd_part(specialities))
            t4 += self.add()
            t5 += self.add_many()
            t6 += self.change(choice = random.randint(1, db))
            t7 += self.change_many(choice1 = random.choice(specialities), choice2 = random.choice(specialities))
            t8 += self.delete_key(choice = random.randint(1, db))
            t9 += self.delete_not_key(choice = fake.name())
            t10 += self.delete_many(choice = fake.name())
            
        t11 += self.compression1(db_name, limit = 200)
        t12 += self.compression2(db_name)
            


        self.avg1 = t1 / num_experiments
        self.avg2 = t2 / num_experiments
        self.avg3 = t3 / num_experiments
        self.avg4 = t4 / num_experiments
        self.avg5 = t5 / num_experiments
        self.avg6 = t6 / num_experiments
        self.avg7 = t7 / num_experiments
        self.avg8 = t8 / num_experiments
        self.avg9 = t9 / num_experiments
        self.avg10 = t10 / num_experiments
        self.avg11 = t11 / num_experiments
        self.avg12 = t12 / num_experiments
        '''print(f"Поиск по ключу занял {avg1}")
        print(f"Поиск по не ключу занял {avg2}")
        print(f"Поиск по маске занял {avg3}")
        print(f"Добавление занял {avg4}")
        print(f"Добаваление группы занял {avg5}")
        print(f"Изменение занял {avg6}")
        print(f"Изменение группы занял {avg7}")
        print(f"Удаленеие по ключу занял {avg8}")
        print(f"Удаленеие по ключу занял {avg9}")
        print(f"Удаление группы занял {avg10}")
        print(f"Сжатие1 занял {avg11}")
        print(f"Сжатие2 занял {avg12}")
        '''