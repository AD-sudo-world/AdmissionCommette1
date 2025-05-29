from django.urls import path
from . import views

app_name = 'statements'

urlpatterns = [
    path('', views.index, name='index'),  # Было views.myStatements (такой функции нет)
    path('add/', views.addStatements, name='addStatements'),
    path('api/directions/', views.api_directions, name='api_directions'),
    path('api/exams/', views.api_direction_exams, name='api_direction_exams')  # Было direction-exams
]