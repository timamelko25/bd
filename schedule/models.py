from django.db import models
from django.forms import ValidationError

    
class Group(models.Model):
    group_number = models.CharField(max_length=255, unique=True)
    speciality = models.ForeignKey('Speciality', on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.group_number   
 
class Discipline(models.Model):
    EXAM_CHOISES = (
        ('зачет', 'зачет'),
        ('экзамен', 'экзамен'),
    )
    name = models.CharField(max_length=255)
    exam = models.CharField(max_length=255, choices=EXAM_CHOISES)
    
    def __str__(self):
        return self.name
    
class Teachers(models.Model):
    name = models.CharField(max_length=255)
    study_discipline = models.ForeignKey(Discipline, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.name
    
class Speciality(models.Model):
    DURATION_CHOISES = (
        ('1','1'),
        ('2','2'),
    )
    
    SEMESTR_CHOISES = (
        ('1','1'),
        ('2','2'),
        ('3','1,2'),
    )
    name = models.CharField(max_length=255)
    disciplines = models.ForeignKey(Discipline, on_delete=models.DO_NOTHING)
    duration_discipline = models.CharField(max_length=255, choices=DURATION_CHOISES)
    semestr_discipline = models.CharField(max_length=50, choices=SEMESTR_CHOISES)
    
    def clean(self):
        if self.duration_discipline == '1' and self.semestr_discipline == '2':
            self.semestr_discipline = '1'
        elif self.duration_discipline == '2' and self.semestr_discipline != '1,2':
            self.semestr_discipline = '1,2'
            
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    speciality = models.ForeignKey(Speciality, on_delete=models.DO_NOTHING)
    study_year = models.CharField(max_length=255)
    is_studying = models.BooleanField(default=True)
    is_gradueted = models.BooleanField(default=False)
    is_expelled = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Schedule(models.Model):
    data = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING)
    discipline = models.ForeignKey(Discipline, on_delete=models.DO_NOTHING)
    semester = models.CharField(max_length=255)
    
    
    def clean(self):
        groups_count = Schedule.objects.filter(teacher=self.teacher, semester=self.semester).count()
        if groups_count >= 2:
            raise ValidationError('Преподаватель может вести не более двух групп в семестре')
        
        # Проверка принадлежности группы к списку групп, которые ведет преподаватель
        if self.group not in Group.objects.filter(teachers=self.teacher):
            raise ValidationError('Группа не принадлежит к списку поставленных групп для этого преподавателя')

        # Проверка принадлежности дисциплины к списку дисциплин, доступных для данной специальности
        if self.discipline not in Discipline.objects.filter(speciality=self.group.speciality):
            raise ValidationError('Дисциплина не принадлежит к списку поставленных занятий для этой специальности')
        
    def __str__(self):
        return self.group
    

class Session(models.Model):
    semestr = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    discipline = models.ForeignKey(Discipline, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING)
    mark = models.ForeignKey('Mark', on_delete=models.DO_NOTHING)
    
    def clean(self):
        # Проверка наличия оценки за этот семестр и год для данного студента и дисциплины
        existing_session = Session.objects.filter(
            student=self.student,
            discipline=self.discipline,
            teacher=self.teacher,
            semestr=self.semestr,
            year=self.year
        ).exists()
        if existing_session:
            raise ValidationError('Уже поставлена оценка за этот семестр и год')

        # Проверка принадлежности студента к специальности, связанной с этой дисциплиной
        if self.discipline not in self.student.speciality.disciplines.all():
            raise ValidationError('Студент не принадлежит к специальности, связанной с этой дисциплиной')



        # Проверка того, что преподаватель ведет эту дисциплину
        if self.teacher.study_discipline != self.discipline:
            raise ValidationError('Преподаватель не ведет эту дисциплину')

    def save(self, *args, **kwargs):
        # Проверка оценки и изменение статуса студента
        if self.mark.mark == '2' or self.mark.mark == 'незачет':
            self.student.is_studying = False
            self.student.is_expelled = True
            self.student.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.student)
    
    
class Mark (models.Model):
    mark = models.CharField(max_length=255)
    
    def __str__(self):
        return self.mark