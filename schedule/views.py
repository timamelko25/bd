from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from schedule.forms import *
from schedule.models import *
from django.db.models import Q
from .database_filing import Data

from schedule.research import Research


def index(request): 
    
    return render(request, 'schedule/index.html')




def schedule(request):
    objects = Schedule.objects.all().order_by('date')

    form = ScheduleForm()

    search_query = request.GET.get('search', '')

    if search_query:
        objects = objects.filter(
            Q(id__icontains=search_query) |
            Q(semester__semester__icontains=search_query) |
            Q(group_group__icontains=search_query) |
            Q(teacher_teacher__icontains=search_query) |
            Q(discipline_discipline__icontains=search_query) |
            Q(date__icontains=search_query)
        )

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Расписание успешно добавлено')
        else:
            messages.error(request, 'Ошибка валидации. Проверьте введенные данные.')
        form = ScheduleForm()

    return render(request, 'schedule/schedule.html', {'objects': objects, 'form': form})




def edit_schedule(request, pk):
    schedule = Schedule.objects.get(id=pk)
    form = ScheduleForm(instance=schedule)
    
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Расписание успешно изменено')
    
    return render(request, 'schedule/edit_schedule.html', {'form': form, 'schedule': schedule})




def session(request):
    objects = Session.objects.all().order_by('student')
    form = SessionForm()
    filter_form = FilterForm()
    
    search_query = request.GET.get('search', '')

    if search_query:
        objects = objects.filter(
            Q(student__name__icontains=search_query) |
            Q(mark__icontains=search_query) |
            Q(year__icontains=search_query) |
            Q(discipline__name__icontains=search_query)
        )
        
    if request.method == 'POST':
        form = SessionForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Оценка успешно добавлена')
        else:
            messages.error(request, 'Ошибка валидации. Проверьте введенные данные.')
        form = SessionForm()
        
        if 'submit_filter_form' in request.POST:
            filter_form = FilterForm(request.POST)
            if filter_form.is_valid():
                year = filter_form.cleaned_data.get('year')
                semestr = filter_form.cleaned_data.get('semestr')
                objects = Session.objects.filter(year=year, semestr=semestr)
            
    elif request.method == 'GET':
        filter_form = FilterForm()
        year = request.GET.get('year')
        semestr = request.GET.get('semestr')
        if year and semestr:
            objects = Session.objects.filter(year=year, semestr=semestr, mark__in=['2', 'незачет'])

    return render(request, 'schedule/session.html', {'form': form, 'objects': objects, 'search_query': search_query, 'filter_form': filter_form})






def teachers(request):   
    objects = Teachers.objects.filter(
        Q(session__mark='2') | 
        Q(session__mark='незачет')
    ).distinct().order_by('study_discipline')
    
    return render(request, 'schedule/teachers.html', {'objects': objects}) 



def students(request): 
    objects = Student.objects.all().order_by('group')
    
    form = StudentForm()
    if request.method == 'POST':
        if 'reactivate_student' in request.POST:
            student_id = request.POST.get('student')
            student = Student.objects.get(id=student_id)
            if student.is_expelled:
                student.is_expelled = False
                student.is_studying = True
                student.study_year = '2025'
                student.save()
                messages.success(request, 'Студент успешно восстановлен')
            else:
                messages.error(request, 'Студент не бьл отчислен')
        form = StudentForm()
        
    return render(request, 'schedule/students.html', {'objects': objects, 'form': form})


def research(request):
    research = Research()
    research.main()
    context = {
        'avg_search_key': research.avg1,
        'avg_search_not_key': research.avg2,
        'avg_search_mask': research.avg3,
        'avg_add': research.avg4,
        'avg_add_many': research.avg5,
        'avg_change': research.avg6,
        'avg_change_many': research.avg7,
        'avg_delete_key': research.avg8,
        'avg_delete_not_key': research.avg9,
        'avg_delete_many': research.avg10,
        'avg_compression1': research.avg11,
        'avg_compression2': research.avg12,
    }
    return render(request, 'schedule/research.html', context)

def database_filing(request):
    data = Data()
    data.main()
    return render(request, 'schedule/database_filing.html')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page Not Found</h1>")