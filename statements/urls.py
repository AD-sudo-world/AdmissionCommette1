from django.urls import path
from . import views

app_name = 'statements'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.addStatements, name='addStatements'),
    path('delete/<int:pk>/', views.delete_application, name='delete_application'),
    path('update/<int:pk>/', views.update_status, name='update_status'),
    path('api/directions/', views.api_directions, name='api_directions'),
    path('api/exams/', views.api_direction_exams, name='api_direction_exams')
]