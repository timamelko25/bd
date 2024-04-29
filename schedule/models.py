from django.db import models
from django.forms import ValidationError

class Group(models.Model):
    group_number = models.CharField(max_length=255, unique=True)
    speciality = models.ForeignKey('Speciality', on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.group_number
    

class Teachers(models.Model):
    name = models.CharField(max_length=255)
    study_discipline = models.ForeignKey('Discipline', on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.name
 
 
 
class Discipline(models.Model):
    EXAM_CHOISES = (
        ('зачет', 'зачет'),
        ('экзамен', 'экзамен'),
    )
    name = models.CharField(max_length=255)
    exam = models.CharField(max_length=255, choices=EXAM_CHOISES)
    
    def __str__(self):
        return self.name
   
    
    

class Speciality(models.Model):
    name = models.CharField(max_length=255)
            
    def __str__(self):
        return self.name


class SpecialityDiscipline(models.Model):
    DURATION_CHOICES = (
        ('1','1'),
        ('2','2'),
    )
    
    SEMESTER_CHOICES = (
        ('1','1'),
        ('2','2'),
        ('3','1,2'),
    )
    
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    duration_discipline = models.CharField(max_length=255, choices=DURATION_CHOICES)
    semester_discipline = models.CharField(max_length=50, choices=SEMESTER_CHOICES)



class Student(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    speciality = models.ForeignKey(Speciality, on_delete=models.DO_NOTHING)
    study_year = models.CharField(max_length=255)
    is_studying = models.BooleanField(default=True)
    is_gradueted = models.BooleanField(default=False)
    is_expelled = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.is_gradueted or self.is_expelled:
            self.is_studying = False
        elif not (self.is_gradueted or self.is_expelled):
            self.is_studying = True
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name





class Schedule(models.Model):
    date = models.DateField()
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING)
    discipline = models.ForeignKey(Discipline, on_delete=models.DO_NOTHING)
    semester = models.CharField(max_length=255)
    
    def clean(self):
        groups_count = Schedule.objects.filter(teacher=self.teacher, semester=self.semester).count()
        if groups_count >= 2:
            raise ValidationError('Преподаватель может вести не более двух групп в семестре')

        if self.discipline not in Discipline.objects.filter(speciality=self.group.speciality):
            raise ValidationError('Дисциплина не принадлежит к списку поставленных занятий для этой специальности')
        
    def __str__(self):
        return self.group
    





class Session(models.Model):
    
    MARK_CHOICES = (
        ('незачет', 'незачет'),
        ('зачет', 'зачет'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    
    semestr = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    discipline = models.ForeignKey(Discipline, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING)
    mark = models.CharField(max_length=255, choices=MARK_CHOICES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  

        if self.mark == '2' or self.mark == 'незачет':
            self.student.is_studying = False
            self.student.is_expelled = True
        self.student.save()

    def __str__(self):
        return str(self.student)
