# from . import database_filing
from . import views
from django.urls import path
from .views import get_group_disciplines, get_discipline_teachers


urlpatterns = [
    path('', views.index, name = 'home'),
    path('index', views.index, name = 'home'), 
    path('schedule', views.schedule, name = 'schedule'),
    path('session', views.session, name = 'session'),
    path('teachers', views.teachers, name = 'teachers'),
    path('students', views.students, name = 'students'),
    path('edit_schedule/<int:pk>/', views.edit_schedule, name='edit_schedule'),
    path('research', views.research, name = 'research'),
    path('database_filing', views.database_filing, name = 'database_filing'),
    path('get_group_disciplines/', get_group_disciplines, name='get_group_disciplines'),
    path('get_discipline_teachers/', get_discipline_teachers, name='get_discipline_teachers'),
]