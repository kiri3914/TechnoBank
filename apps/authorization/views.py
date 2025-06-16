from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .forms import CustomUserRegistrationForm
from .models import CustomUser



def register(request):
    if request.method == 'POST':
        print(request.POST)
        form = CustomUserRegistrationForm(request.POST, request.FILES) # request.POST это дикт с данными пользователя {'phone_number': "+773217836"}
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = CustomUser.objects.filter(phone_number=phone_number).first()
        if user is None:
            messages.error(request, f'Пользователь с номером {phone_number} не найден!')
            return redirect('login_user')

        if not user.check_password(password):
            messages.error(request, ' Неверный пароль')
            return redirect('login_user')
        
        login(request, user)
        messages.success(request, 'Вы успешно зашли в Аккаунт')
        return redirect('index')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('index')



# GET - для получения данных
# POST
# PUT
# PATCH
# DELETE