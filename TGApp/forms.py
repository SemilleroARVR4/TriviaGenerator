from cProfile import label
from pyexpat import model
from django import forms
from django.forms import ModelForm
from .models import Pregunta, Trivia, PreguntaQuiz, ElegirRespuesta, PreguntasRespondidasTrivia, PreguntaQuiz, PreguntasConOpciones, Poll

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

class ElegirRespuestaTest(forms.ModelForm):
    class Meta:
        model = ElegirRespuesta
        fields = ["pregunta", "correcta", "texto",]
        # labels = {'texto':"Enunciado de la pregunta"}

class formTrivia(forms.BaseInlineFormSet):
    class Meta:
        model = Trivia
        fields = ['autor', 'nombre', 'Tipo']
        labels = {'autor' : "Creador", 'nombre' : "Nombre Trivia", 'Tipo' : "Tipo Trivia"}

        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder':'Nombre de la trivia'}), 
            'Tipo': forms.TextInput(attrs={'placeholder':'Tipo de trivia'}),  
        }
    
class formTrivia(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ["pregunta", "opcionCorrecta", "opcion2", "opcion3", "opcion4"]


#VIDEO

class ElegirInLineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(ElegirInLineFormset, self).clean()

        respuesta_correcta = 0
        for formulario in self.forms:
            if not formulario.is_valid():
                return 

            if formulario.cleaned_data and formulario.cleaned_data.get('correcta') is True:
                respuesta_correcta += 1

        try: 
            assert respuesta_correcta == PreguntaQuiz.NUMERO_DE_RESPUESTAS_PERMITIDAS
        except AssertionError: 
            raise forms.ValidationError('Exactamente una sola respuesta es permitida')



class OtroModelo(forms.ModelForm):
    class Meta:
        model: Pregunta
        fields = "__all__"


class formQuiz(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ["pregunta", "opcionCorrecta", "opcion2", "opcion3", "opcion4",]
        labels = {'pregunta': "Pregunta",'opcionCorrecta': "Opcion 1",'opcion2': "Opcion 2",'opcion3': "Opcion 3",
        'opcion4': "Opcion 4", 'respuesta': "Respuesta de la pregunta"}
        
        # fields = ["trivia", "pregunta", "opcionCorrecta", "opcion2", "opcion3", "opcion4",]
        # labels = {'trivia': "Tipo Trivia", 'pregunta': "Pregunta",'opcionCorrecta': "Opcion correcta",'opcion2': "Opcion 2",'opcion3': "Opcion 3",'opcion4': "Opcion 4",}
        
        
        widgets = {
            
            'pregunta': forms.Textarea(attrs={'placeholder':'Enunciado de la pregunta'}),
            'opcionCorrecta': forms.Textarea(attrs={'placeholder':'Opcion 1'}), 
            'opcion2': forms.Textarea(attrs={'placeholder':'Opcion 2'}), 
            'opcion3': forms.Textarea(attrs={'placeholder':'Opcion 3'}), 
            'opcion4': forms.Textarea(attrs={'placeholder':'Opcion 4'}), 
            'respuesta': forms.Textarea(attrs={'placeholder':'Respuesta a la pregunta'}), 
        }

class CreatePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'option_one', 'option_two', 'option_three']