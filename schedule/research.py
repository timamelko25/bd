import time
import random 
from schedule.models import Group, Student
from django.db.models import Q

class Research():
    def search_key(self, choice):
        start_time = time.time()

        Student.objects.filter(id = choice).exists()

        end_time = time.time()
        return end_time - start_time

    def search_not_key(self, choice):
        start_time = time.time()

        Student.objects.filter(Q(speciality = choice)).exists()

        end_time = time.time()
        return end_time - start_time

    def search_mask(self, choice):
        start_time = time.time()

        Student.objects.filter(speciality__name__icontains=choice).exists()

        end_time = time.time()
        return end_time - start_time

    def add(self):
        start_time = time.time()
        group = random.choice(Group.objects.all())
        Student.objects.create(
            name = "Timofey",
            group = group,
            speciality = group.speciality,
            study_year = 2024
        )
        end_time = time.time()
        return end_time - start_time

    def add_many(self):
        start_time = time.time()
        group = random.choice(Group.objects.all())
        Student.objects.bulk_create([
            Student(
                name = "Timofey",
                group = group,
                speciality = group.speciality,
                study_year = 2024
            ),
            Student(
                name = "Egor",
                group = group,
                speciality = group.speciality,
                study_year = 2024
            )
        ])
        end_time = time.time()
        return end_time - start_time

    def change(self, choice):
        start_time = time.time()
        Student.objects.filter(id = choice).update(
            name = "CHANDED NAME",
        )
        end_time = time.time()
        return end_time - start_time

    def change_many(self, choice1, choice2):
        start_time = time.time()
        tmp1 = Student.objects.filter(speciality=choice1).first()
        tmp2 = Student.objects.filter(speciality=choice2).first()

        if tmp1 and tmp2:
            tmp1.name = "CHANDED NAME"
            tmp2.name = "CHANDED NAME2"
        
            Student.objects.bulk_update([tmp1, tmp2], ["name", "name"])

        end_time = time.time()
        return end_time - start_time

    def delete_key(self, choice):
        start_time = time.time()
        student = Student.objects.filter(id=choice)
        student.delete()
        end_time = time.time()
        return end_time - start_time

    def delete_many(self):
        start_time = time.time()
        student = Student.objects.filter(speciality = 1)
        student.delete()
        end_time = time.time()
        return end_time - start_time

    def compression1(self):
        start_time = time.time()
        students_to_delete = Student.objects.all().order_by('id')[:200]
        student_id_to_delete = students_to_delete.values_list('id', flat=True)
        tmp = Student.objects.filter(id__in=student_id_to_delete)
        tmp.delete()
        end_time = time.time()
        return end_time - start_time


    def compression2(self):
        start_time = time.time()
        tmp = Student.objects.all()
        students_to_delete = Student.objects.all().order_by('id')[:(len(tmp)-200)]
        student_id_to_delete = students_to_delete.values_list('id', flat=True)
        tmp1 = Student.objects.filter(id__in=student_id_to_delete)
        tmp1.delete()
        end_time = time.time()
        return end_time-start_time

    def main(self):
        total_time = 0
        num_experiments = 100
        for _ in range(num_experiments):
            total_time += self.search_key(choice = random.randint(1, 1000))

        average_time = total_time / num_experiments
        print(f"Поиск по ключу занял {average_time}")
    
        total_time = 0
        num_experiments = 100
        for _ in range(num_experiments):
            total_time += self.search_not_key(1)

        average_time = total_time / num_experiments
        print(f"Поиск по не ключу занял {average_time}")
        
        total_time = 0
        num_experiments = 100
        for _ in range(num_experiments):
            total_time += self.search_mask("Прог")

        average_time = total_time / num_experiments
        print(f"Поиск по маске занял {average_time}")
        
        total_time = 0
        num_experiments = 100
        for _ in range(num_experiments):
            total_time += self.add()

        average_time = total_time / num_experiments
        print(f"Добавление занял {average_time}")
        
        total_time = 0
        num_experiments = 100
        for _ in range(num_experiments):
            total_time += self.add_many()

        average_time = total_time / num_experiments
        print(f"Добаваление группы занял {average_time}")
        
        total_time = 0
        num_experiments = 100
        for _ in range(num_experiments):
            total_time += self.change(random.randint(1, 1000))

        average_time = total_time / num_experiments
        print(f"Изменение занял {average_time}")
        
        total_time = 0
        num_experiments = 100
        for _ in range(num_experiments):
            total_time += self.change_many(1, 2)

        average_time = total_time / num_experiments
        print(f"Изменение группы занял {average_time}")
        
        total_time = 0
        num_experiments = 100
        for _ in range(num_experiments):
            total_time += self.delete_key(random.randint(1,1000))

        average_time = total_time / num_experiments
        print(f"Удаленеие по ключу занял {average_time}")
        
        total_time = 0
        num_experiments = 100
        for _ in range(num_experiments):
            total_time += self.delete_many()

        average_time = total_time / num_experiments
        print(f"Удаление группы занял {average_time}")
        
        total_time = 0
        num_experiments = 1
        for _ in range(num_experiments):
            total_time += self.compression1()

        average_time = total_time / num_experiments
        print(f"Сжатие1 занял {average_time}")
        
        total_time = 0
        num_experiments = 1
        for _ in range(num_experiments):
            total_time += self.compression2()

        average_time = total_time / num_experiments
        print(f"Сжатие2 занял {average_time}")
    

