from django.urls import path
from accounts import views
from django.urls import path, include
app_name = 'accounts'

urlpatterns = [
    path('', views.vxod, name='index'),
    path('registr/', views.registr, name='registr'),
]