from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile

@login_required
def personal(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    context = {
        'title': 'Личный кабинет',
        'profile': profile,
        'user': request.user
    }
    return render(request, 'userprofile/personal.html', context)

@login_required
def personalAdd(request):
    profile = request.user.profile
    context = {
        'profile': profile,
        'user': request.user
    }
    return render(request, 'userprofile/personalAdd.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        try:
            user = request.user
            profile = user.profile
            
            # Обновление данных пользователя
            user.last_name = request.POST.get('last_name', '')
            user.first_name = request.POST.get('first_name', '')
            user.email = request.POST.get('email', '')
            user.save()
            
            # Обновление профиля
            profile.middle_name = request.POST.get('middle_name', '')
            profile.birth_date = request.POST.get('birth_date') or None
            profile.phone = request.POST.get('phone', '')
            profile.doc_type = request.POST.get('doc_type', 'passport')
            profile.dormitory_needed = request.POST.get('dormitory') == 'yes'
            
            # Обработка документа
            doc_data = request.POST.get('doc_number', '').split()
            if len(doc_data) >= 2:
                profile.doc_series = doc_data[0]
                profile.doc_number = doc_data[1]
            else:
                profile.doc_series = ''
                profile.doc_number = ''
            
            profile.save()
            
            messages.success(request, 'Профиль успешно обновлен')
            return redirect('userprofile:index')
            
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении: {str(e)}')
    
    return redirect('userprofile:personalAdd')