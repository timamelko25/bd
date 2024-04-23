from django import forms
from .models import *

class SessionForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), label='Студент', empty_label='')
    semestr = forms.IntegerField(label='Семестр', min_value=1, max_value=2)
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), label='Дисциплина', empty_label='')
    mark = forms.ModelChoiceField(queryset=Mark.objects.all(), label='Оценка', empty_label='')
    year = forms.IntegerField(label='Год', min_value=2000, max_value=2004)
    
    class Meta:
        model = Session
        fields = '__all__'
        
class ScheduleForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='Группа', empty_label='')
    semester = forms.IntegerField(label='Семестр', min_value=1, max_value=2)
    teacher = forms.ModelChoiceField(queryset=Teachers.objects.all(), label='Преподаватель', empty_label='')
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), label='Дисциплина', empty_label='')
    data = forms.CharField(max_length=255, label='Дата проведения')
    
    class Meta:
        model = Schedule
        fields = '__all__'   
        
        
class StudentForm (forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), label='Студент', empty_label='')
    class Meta:
        model = Student
        fields = '__all__'