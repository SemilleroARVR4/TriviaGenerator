from pyexpat import model
from django import forms
from django.forms import ModelForm
from .models import Pregunta, Trivia, Admin

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = '__all__'

# class RegistroFormulario(UserCreationForm):
#     #proporciona 3 parametros
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)

#     class Meta:
#         model = User

#         fields = [
#             'first_name',
#             'last_name',
#             'username',
#             'email',
#             'password1',
#             'password2',
#         ]

class formularioTest(forms.ModelForm):
    enunciado = forms.CharField(max_length=200)

# class formTrivia(ModelForm):
#     class Meta:
#         model = Trivia
#         fields = ['autor', 'nombre', 'Tipo']
    # autor = forms.ModelChoiceField(queryset=Trivia.objects.all())
    # nombre = forms.CharField(max_length=100)
    # Tipo = forms.CharField(max_length=100)


class formTest(forms.Form):
    nombre = forms.CharField(label="Etiqueta", required=True)
    email = forms.EmailField(label="Correo")