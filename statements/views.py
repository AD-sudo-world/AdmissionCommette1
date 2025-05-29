from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Faculty, Direction, Application, DirectionExam
from django.http import JsonResponse

@login_required
def addStatements(request):
    if request.method == 'POST':
        direction_id = request.POST.get('direction')
        try:
            direction = Direction.objects.get(id=direction_id)
            application = Application.objects.create(
                user=request.user,
                direction=direction,
                status='submitted'
            )
            # Здесь обработка экзаменов и других данных
            return redirect('statements:index')
        except Direction.DoesNotExist:
            return render(request, 'statements/addStatements.html', {
                'error': 'Выберите корректное направление',
                'faculties': Faculty.objects.all()
            })
    
    return render(request, 'statements/addStatements.html', {
        'faculties': Faculty.objects.all()
    })

def api_directions(request):
    faculty_id = request.GET.get('faculty_id')
    directions = Direction.objects.filter(faculty_id=faculty_id).values('id', 'code', 'name')
    return JsonResponse(list(directions), safe=False)

def api_direction_exams(request):
    direction_id = request.GET.get('direction_id')
    exams = DirectionExam.objects.filter(direction_id=direction_id).select_related('exam').values(
        'id', 'exam__id', 'exam__name', 'exam__min_score', 'exam__max_score', 'required'
    )
    return JsonResponse(list(exams), safe=False)

@login_required
def myStatements(request):
    # Получаем все заявления текущего пользователя
    applications = Application.objects.filter(user=request.user)
    
    context = {
        'applications': applications,
        'title': 'Мои заявления'
    }
    return render(request, 'statements/myStatements.html', context)