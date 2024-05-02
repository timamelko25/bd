# from . import database_filing
from . import views
from django.urls import path


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
]