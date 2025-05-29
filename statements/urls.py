from django.urls import path
from statements import views
from django.urls import path, include
app_name = 'statements'

urlpatterns = [
    path('', views.myStatements, name='index'),
    path('addStatements/', views.addStatements, name='addStatements'),
    path('api/directions/', views.api_directions, name='api_directions'),
    path('api/direction-exams/', views.api_direction_exams, name='api_direction_exams')
]