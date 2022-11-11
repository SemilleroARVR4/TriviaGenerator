from cProfile import label
from pyexpat import model
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
        fields = ["autor", "trivia", "pregunta", "opcionCorrecta", "opcion2", "opcion3", "opcion4",]
        labels = {'autor' : "Creador", 'trivia': "Tipo Trivia", 'pregunta': "Pregunta",'opcionCorrecta': "Opcion correcta",'opcion2': "Opcion 2",'opcion3': "Opcion 3",'opcion4': "Opcion 4",}
        
        # fields = ["trivia", "pregunta", "opcionCorrecta", "opcion2", "opcion3", "opcion4",]
        # labels = {'trivia': "Tipo Trivia", 'pregunta': "Pregunta",'opcionCorrecta': "Opcion correcta",'opcion2': "Opcion 2",'opcion3': "Opcion 3",'opcion4': "Opcion 4",}
        
        
        widgets = {
            
            'autor': forms.HiddenInput(),
            'trivia': forms.HiddenInput(),
            'pregunta': forms.Textarea(attrs={'placeholder':'Enunciado de la pregunta'}),
            'opcionCorrecta': forms.Textarea(attrs={'placeholder':'Opcion correcta'}), 
            'opcion2': forms.Textarea(attrs={'placeholder':'Opcion incorrecta 1'}), 
            'opcion3': forms.Textarea(attrs={'placeholder':'Opcion incorrecta 2'}), 
            'opcion4': forms.Textarea(attrs={'placeholder':'Opcion incorrecta 3'}), 
        }

class formTrivia(forms.ModelForm):
    class Meta:
        model = Trivia
        fields = ['autor', 'nombre', 'Tipo']
        labels = {'autor' : "Creador", 'nombre' : "Nombre Trivia", 'Tipo' : "Tipo Trivia"}

        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder':'Nombre de la trivia'}), 
            'Tipo': forms.TextInput(attrs={'placeholder':'Tipo de trivia'}),  
        }
    