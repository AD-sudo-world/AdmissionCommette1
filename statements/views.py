from django.shortcuts import render

# Create your views here.
def myStatements(request):
    return render(request, 'statements/myStatements.html')


def addStatements(request):
    return render(request, 'statements/addStatements.html')