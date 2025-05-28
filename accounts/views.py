from django.shortcuts import render
from django.shortcuts import HttpResponse

def registr(request):
    return render(request, 'accounts/registr.html')


def vxod(request):
    return render(request, 'accounts/vxod.html')
