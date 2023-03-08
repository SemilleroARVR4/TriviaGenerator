from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models


class UserRegisterFormAdmin(UserCreationForm):
    email = forms.EmailField()
    codigo = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'email', 'codigo', 'password1', 'password2']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

