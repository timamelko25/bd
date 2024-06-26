from tkinter import Widget
from django import forms
from .models import *



class SessionForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.filter(is_studying = True).order_by('name'), label='Студент', empty_label='')
    semestr = forms.IntegerField(label='Семестр', min_value=1, max_value=2)
    teacher = forms.ModelChoiceField(queryset=Teachers.objects.all().order_by('name'), label='Преподаватель', empty_label='')
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all().order_by('name'), label='Дисциплина', empty_label='')
    year = forms.IntegerField(label='Год', min_value=2000, max_value=2024)
    
    class Meta:
        model = Session
        fields = ['year', 'semestr', 'student', 'discipline', 'teacher', 'mark']
        widgets = {
            'mark': forms.Select(choices=Session.MARK_CHOICES)
        }
        
        
        
class ScheduleForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='Группа', empty_label='')
    semester = forms.IntegerField(label='Семестр', min_value=1, max_value=2)
    teacher = forms.ModelChoiceField(queryset=Teachers.objects.all().order_by('name'), label='Преподаватель', empty_label='')
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all().order_by('name'), label='Дисциплина', empty_label='')
    date = forms.DateField(label='Дата', widget=forms.TextInput(attrs={'class': 'datepicker'}))
    
    class Meta:
        model = Schedule
        fields = ['date', 'semester', 'group', 'discipline', 'teacher']
        
        
        
        
class StudentForm (forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.filter(is_expelled = True).order_by('name'), label='Студент', empty_label='')
    class Meta:
        model = Student
        
        
class FilterForm(forms.Form):
    SEMESTR_CHOICES = (
        ('1', '1'),
        ('2', '2'),
    )

    YEAR_CHOICES = [(str(year), str(year)) for year in range(2000, 2025)]

    year = forms.ChoiceField(label='Год', choices=YEAR_CHOICES)
    semestr = forms.ChoiceField(label='Семестр', choices=SEMESTR_CHOICES)