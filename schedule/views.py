from itertools import count
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib import messages
from schedule.forms import *
from schedule.models import *
from django.db.models import Q, Count

def index(request): 
    return render(request, 'schedule/index.html')

def schedule(request):
    objects = Schedule.objects.all().order_by('group')
    form = ScheduleForm()

    search_query = request.GET.get('search', '')

    if search_query:
        objects = objects.filter(
            Q(group_group__icontains=search_query) |
            Q(teacher_teacher__icontains=search_query) |
            Q(discipline_discipline__icontains=search_query) |
            Q(data__icontains=search_query)
        )

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Расписание успешно добавлено')
            return redirect('schedule/schedule.html')
        else:
            form = ScheduleForm()

    return render(request, 'schedule/schedule.html', {'objects': objects, 'form': form})

def session(request):
    objects = Session.objects.all().order_by('student')
    form = SessionForm()
    
    search_query = request.GET.get('search', '')

    if search_query:
        objects = objects.filter(
            Q(student__name__icontains=search_query) |
            Q(mark__mark__icontains=search_query) |
            Q(year__icontains=search_query) |
            Q(discipline__name__icontains=search_query)
        )
        
    if request.method == 'POST':
        form = SessionForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Расписание успешно добавлено')
            return redirect('schedule/schedule.html')
        else:
            form = SessionForm()

    return render(request, 'schedule/session.html', {'form': form, 'objects': objects, 'search_query': search_query})

def teachers(request): 
    # objects = Teachers.objects.all().order_by('study_discipline')    
    objects = Teachers.objects.filter(
        Q(session__mark__mark='2') | 
        Q(session__mark__mark='незачет')
    ).distinct().order_by('study_discipline')
    return render(request, 'schedule/teachers.html', {'objects': objects}) 

def students(request): 
    objects = Student.objects.all().order_by('group')
    
    form = StudentForm()
    if request.method == 'POST':
        if 'reactivate_student' in request.POST:  # Если нажата кнопка "Восстановить студента"
            if Student.is_expelled:  # Проверяем, является ли студент отчислен
                # Изменяем статус студента на "учится" и устанавливаем год обучения 2025
                Student.is_studying = True
                Student.study_year = '2025'
    else:
        form = StudentForm()
        
    return render(request, 'schedule/students.html', {'objects': objects, 'form': form}) 

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page Not Found</h1>")