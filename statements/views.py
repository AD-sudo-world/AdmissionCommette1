from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Faculty, Direction, DirectionExam, Application
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegrityError

@login_required
def index(request):
    if request.user.is_superuser:
        # Для суперпользователя - все заявления с возможностью изменения статуса
        applications = Application.objects.all().order_by('-created_at')
        return render(request, 'statements/admin_applications.html', {
            'applications': applications,
            'is_admin': True
        })
    else:
        # Для обычного пользователя - только его заявления
        applications = Application.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'statements/myStatements.html', {
            'applications': applications,
            'is_admin': False
        })

@login_required
def update_status(request, pk):
    if not request.user.is_superuser:
        return redirect('statements:index')
    
    if request.method == 'POST':
        application = get_object_or_404(Application, pk=pk)
        new_status = request.POST.get('status')
        
        if new_status in dict(Application.STATUS_CHOICES).keys():
            application.status = new_status
            application.save()
            messages.success(request, 'Статус заявления успешно обновлен')
        else:
            messages.error(request, 'Неверный статус')
            
    return redirect('statements:index')

@login_required
def addStatements(request):
    if request.user.is_superuser:
        messages.warning(request, 'Администраторы не могут подавать заявления')
        return redirect('statements:index')
    
    """Страница подачи заявления с факультетами и направлениями"""
    if request.method == 'POST':
        # Здесь должна быть логика обработки формы и сохранения заявления
        # Например:
        try:
            direction_id = request.POST.get('direction')
            if not direction_id:
                messages.error(request, 'Не выбрано направление')
                return redirect('statements:addStatements')
            
            direction = Direction.objects.get(pk=direction_id)
            
            # Проверяем, не подано ли уже заявление на это направление
            if Application.objects.filter(user=request.user, direction=direction).exists():
                messages.error(request, 'Вы уже подавали заявление на это направление')
                return redirect('statements:addStatements')
            
            # Создаем заявление
            application = Application.objects.create(
                user=request.user,
                direction=direction,
                status='На рассмотрении'  # Используем значение из STATUS_CHOICES
            )
            
            messages.success(request, 'Заявление успешно подано!')
            return redirect('statements:index')
            
        except IntegrityError:
            # Обработка случая, когда заявление уже существует (на случай race condition)
            messages.error(request, 'Вы уже подавали заявление на это направление')
            return redirect('statements:addStatements')
            
        except Exception as e:
            messages.error(request, f'Ошибка при подаче заявления: {str(e)}')
    
    faculties = Faculty.objects.all().order_by('name')
    return render(request, 'statements/addStatements.html', {
        'faculties': faculties
    })

@login_required
def delete_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    
    # Проверяем, что пользователь может удалять только свои заявления
    # (или является администратором)
    if not request.user.is_superuser and application.user != request.user:
        messages.error(request, 'Вы не можете удалить это заявление')
        return redirect('statements:index')
    
    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Заявление успешно удалено')
        return redirect('statements:index')
    
    # Для GET запроса просто перенаправляем на список заявлений
    return redirect('statements:index')


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