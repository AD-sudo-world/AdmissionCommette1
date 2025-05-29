from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Profile
from django.utils.translation import gettext_lazy as _

@login_required
def personal(request):
    """Отображение личного кабинета"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Создаем профиль, если его нет
        profile = Profile.objects.create(user=request.user)
        messages.info(request, _('Для вас создан новый профиль. Заполните данные.'))
    
    context = {
        'title': _('Личный кабинет'),
        'profile': profile,
        'user': request.user
    }
    return render(request, 'userprofile/personal.html', context)

@login_required
def personalAdd(request):
    """Страница редактирования профиля"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
        messages.info(request, _('Для вас создан новый профиль. Заполните данные.'))
    
    context = {
        'title': _('Редактирование профиля'),
        'profile': profile,
        'user': request.user,
        'doc_types': Profile.DocType.choices  # Добавляем варианты типов документов
    }
    return render(request, 'userprofile/personalAdd.html', context)

@login_required
def update_profile(request):
    """Обновление данных профиля"""
    if request.method == 'POST':
        try:
            user = request.user
            profile = user.profile
            
            # Валидация данных
            email = request.POST.get('email', '').strip()
            if email and '@' not in email:
                raise ValidationError(_('Некорректный email'))
            
            # Обновление данных пользователя
            user.last_name = request.POST.get('last_name', '').strip()
            user.first_name = request.POST.get('first_name', '').strip()
            user.email = email
            user.save()
            
            # Обновление профиля
            profile.middle_name = request.POST.get('middle_name', '').strip()
            profile.birth_date = request.POST.get('birth_date') or None
            profile.phone = request.POST.get('phone', '').strip()
            profile.doc_type = request.POST.get('doc_type', Profile.DocType.PASSPORT)
            profile.dormitory_needed = request.POST.get('dormitory') == 'on'
            
            # Обработка документа
            doc_number = request.POST.get('doc_number', '').strip()
            if doc_number:
                doc_parts = doc_number.split()
                if len(doc_parts) >= 2:
                    profile.doc_series = doc_parts[0]
                    profile.doc_number = ' '.join(doc_parts[1:])
                else:
                    profile.doc_series = ''
                    profile.doc_number = doc_number
            
            profile.full_clean()  # Валидация модели
            profile.save()
            
            messages.success(request, _('Профиль успешно обновлен'))
            return redirect('userprofile:personal')
            
        except ValidationError as e:
            messages.error(request, _('Ошибка валидации: ') + str(e))
        except Exception as e:
            messages.error(request, _('Произошла ошибка при обновлении профиля'))
            # Логирование ошибки (можно добавить logger.error здесь)
    
    return redirect('userprofile:personalAdd')