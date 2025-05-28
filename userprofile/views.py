from django.shortcuts import render

# Create your views here.
def personal(request):
    return render(request, 'userprofile/personal.html')


def personalAdd(request):
    return render(request, 'userprofile/personalAdd.html')