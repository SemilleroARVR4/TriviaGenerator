from cProfile import label
from pyexpat import model
from tkinter import Widget
from django import forms
from django.forms import ModelForm
from .models import Pregunta, Trivia, Admin

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = '__all__'

class formPregunta(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ["Trivia", "pregunta", "opcionCorrecta", "opcion2", "opcion3", "opcion4",]
        labels = {'Trivia': "Nombre Trivia", 'pregunta': "Pregunta",'opcionCorrecta': "Opcion correcta",'opcion2': "Opcion 2",'opcion3': "Opcion 3",'opcion4': "Opcion 4",}
        # Widget = {"pregunta":"pregunta"}

class formTrivia(forms.ModelForm):
    class Meta:
        model = Trivia
        fields = ['autor', 'nombre', 'Tipo']
        labels = {'autor' : "Creador", 'nombre' : "Nombre Trivia", 'Tipo' : "Tipo Trivia"}
    