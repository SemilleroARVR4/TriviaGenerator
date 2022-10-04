from cProfile import label
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

class formPregunta(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ["Trivia", "pregunta", "opcionCorrecta", "opcion2", "opcion3", "opcion4",]
        labels = {'Trivia': "Nombre Trivia", 'pregunta': "Pregunta",'opcionCorrecta': "Opcion correcta",'opcion2': "Opcion 2",'opcion3': "Opcion 3",'opcion4': "Opcion 4",}

class formTrivia(forms.ModelForm):
    class Meta:
        model = Trivia
        fields = ['nombre', 'Tipo']
        labels = {'nombre' : "Nombre Trivia", 'Tipo' : "Tipo Trivia"}