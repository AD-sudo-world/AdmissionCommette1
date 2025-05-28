from django.urls import path
from userprofile import views
from django.urls import path, include
app_name = 'userprofile'

urlpatterns = [
    path('', views.personal, name='index'),
    path('personalAdd/', views.personalAdd, name='personalAdd'), 
]