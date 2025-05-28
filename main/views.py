from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
def index(request):
    context={
        'title': 'Приемная комиссия ИГХТУ',
        'content': "Добро пожаловать в ХИМТЕХ!"
    }
    return render(request, 'main/index.html', context)

def about(request):
    context={
        'title': 'Миссия ИГХТУ',
        'content': "Миссия ИГХТУ",
        'text_on_page':"Мы работаем для того, чтобы обеспечить всем обучающимся в вузе хороший карьерный старт и профессиональные перспективы на рынке труда."
    }
    return render(request, 'main/about.html', context)