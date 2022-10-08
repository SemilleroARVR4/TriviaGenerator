from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.

def registrar(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f'¡Tu cuenta ha sido creada! Ahora puedes ingresar')
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, "users/registrar.html", {'form':form})

def login(request):
    return render(request, "users/login.html")
