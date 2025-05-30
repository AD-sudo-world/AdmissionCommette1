from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Faculty, Direction, DirectionExam, Application

@login_required
def index(request):
    """Страница с заявлениями пользователя"""
    applications = Application.objects.filter(user=request.user).select_related(
        'direction', 'direction__faculty'
    ).order_by('-created_at')
    
    return render(request, 'statements/myStatements.html', {
        'applications': applications
    })

@login_required
def addStatements(request):
    """Страница подачи заявления с факультетами и направлениями"""
    faculties = Faculty.objects.all().order_by('name')
    return render(request, 'statements/addStatements.html', {
        'faculties': faculties
    })

def api_directions(request):
    """API для получения направлений по факультету"""
    faculty_id = request.GET.get('faculty_id')
    if not faculty_id:
        return JsonResponse([], safe=False)
    
    directions = Direction.objects.filter(
        faculty_id=faculty_id
    ).order_by('code').values('id', 'code', 'name')
    
    return JsonResponse(list(directions), safe=False)

def api_direction_exams(request):
    direction_id = request.GET.get('direction_id')
    if not direction_id:
        return JsonResponse([], safe=False)
    
    exams = DirectionExam.objects.filter(
        direction_id=direction_id
    ).select_related('exam')
    
    exam_data = [{
        'id': de.exam.pk,  # используем pk вместо id
        'name': de.exam.name,
        'min_score': de.exam.min_score,
        'max_score': de.exam.max_score,
        'required': de.required
    } for de in exams]
    
    return JsonResponse(exam_data, safe=False)