from django.urls import path
from statements import views
from django.urls import path, include
app_name = 'statements'

urlpatterns = [
    path('', views.myStatements, name='index'),
    path('addStatements/', views.addStatements, name='addStatements'),
]