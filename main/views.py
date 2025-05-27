from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
def index(request):

    context: dict ={
        'title': 'Home',
        'content': 'Главная страница Комиссии - HOME'
    }
    return render(request,'main/index.html', context)

def about(request):
    return HttpResponse('About page')