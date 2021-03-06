from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import logout, authenticate
from .forms import UserRegisterForm, LoginForm, CaptchaUserCreationForm,CaptchaField
from .models import User
from .functions import LogIn
from django.http import HttpResponseRedirect


def userlogin(request):
    if request.method == 'POST':
        if 'register_form' in request.POST:
            user_register = UserRegisterForm(request.POST)
            if user_register.is_valid():
                User.objects.create_user(username=user_register.cleaned_data['username'],
                                         email=user_register.cleaned_data['email'],
                                         password=user_register.cleaned_data['password'],
                                         first_name=user_register.cleaned_data['first_name'])
                LogIn(request, user_register.cleaned_data['username'],user_register.cleaned_data['password'])
                return redirect('home')
        if 'login_form' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                LogIn(request, login_form.cleaned_data['username'],
                      login_form.cleaned_data['password'])
                user = User.objects.get(username = login_form.cleaned_data['username'])
                #user = User.objects.filter(request.user.username == login_form.cleaned_data['username'])
                if user.tipo == 'NT' :
                    return redirect('http://localhost:8000/nutriologo/')

                elif user.tipo == 'AM':
                    return redirect('http://localhost:8000/administrador')
                return redirect('http://localhost:8000/paciente')
    else:
        user_register = UserRegisterForm()
        login_form = LoginForm()
    return render(request, 'users/login.html', {'user_register': user_register, 'login_form': login_form })

def Captcha(request):
    if request.POST:
        form = CaptchaUserCreationForm(request.POST)
    if form.is_valid():
        return HttpResponseRedirect('/?ok')
    else:
        form = CaptchaUserCreationForm()


def LogOut(request):
    logout(request)
    return redirect('/')




