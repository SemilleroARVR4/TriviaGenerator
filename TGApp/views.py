from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pregunta, Trivia, QuizUsuario, QuizUsuarioTrivia, PreguntaQuiz, PreguntasRespondidasTrivia, ElegirRespuesta
from .forms import formPregunta, formTrivia, ElegirRespuestaTest, OtroModelo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import random


# Create your views here.

def inicio(request):
    return render(request, "TGApp/inicio.html")

def nosotros(request):
    return render(request, "TGApp/nosotros.html")

@login_required
def crear(request):
    
    context = {
        'trivias': Trivia.objects.all(),
        'preguntas': Pregunta.objects.all(),
    }
    
    return render(request, "TGApp/index.html", context)


@login_required
def crearPregunta(request, Trivia_id):

    trivias= Trivia.objects.get(id=Trivia_id)
    preguntas = Pregunta.objects.filter(trivia=trivias)
    
    initial_data = {
        'trivia': trivias,
        'autor': request.user,
    }   

    if request.method=='POST':
        formulario = formPregunta(request.POST, initial=initial_data) 
        if formulario.is_valid():
            formulario.save()
            messages.success(request, f'¡Tu pregunta ha sido registrada!' )
            return redirect("/preguntas")
    else:
        formulario = formPregunta(initial=initial_data)
    return render(request, "TGApp/crear.html", {'trivias': trivias, 'preguntas':preguntas, 'formulario': formulario}) 


class CrearNuevaTrivia(SuccessMessageMixin, CreateView):
    model = Trivia
    template_name = 'TGApp/formTrivia.html'
    fields = ['nombre', 'Tipo']
    success_message = "¡Tu trivia ha sido registrada, ya puedes agregar preguntas!"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(CrearNuevaTrivia, self).get_form(form_class)
        form.fields['nombre'].widget.attrs ={'placeholder': 'Nombre de la trivia'}
        form.fields['Tipo'].widget.attrs ={'placeholder': 'Tipo de trivia'}
        return form
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class EditarPregunta(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Pregunta
    template_name = 'TGApp/editarPregunta.html'
    fields = ["trivia", "pregunta", "opcionCorrecta", "opcion2", "opcion3", "opcion4",]
    success_message = "¡Tu pregunta ha sido actualizada correctamente!"
    success_url = reverse_lazy('preguntas')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    #funcion que usa el usuario para poder modificar cosas solo creadas por el 
    def test_func(self):
        Pregunta = self.get_object()
        if self.request.user == Pregunta.autor:
            return True
        return False


class EliminarPregunta(SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Pregunta
    template_name = 'TGApp/eliminarPregunta.html'
    success_url = reverse_lazy('preguntas')
    success_message = "¡Tu pregunta ha sido eliminada correctamente!"

    # def form_valid(self, form):
    #     form.instance.autor = self.request.user
    #     return super().form_valid(form)

    def test_func(self):
        Pregunta = self.get_object()
        if self.request.user == Pregunta.autor:
            return True
        return False


def preguntas(request):
    context = {
        'trivias': Trivia.objects.all().order_by('-id'),
        'preguntas': Pregunta.objects.all().order_by('-id'),
    }
    return render(request, "TGApp/preguntas.html", context)


def correcto(request):
    context = {
        'preguntas': Pregunta.objects.all(),
    }
    return render(request, "TGApp/correcto.html", context)




class Quizz(DetailView):
    model = Pregunta



#VIDEO

def jugarQuiz(request):
    QuizUser, created = QuizUsuarioTrivia.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        pregunta_pk = request.POST.get('pregunta_pk')
        pregunta_respondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
        respuesta_pk = request.POST.get('respuesta_pk')

        try:
            opcion_selecionada = pregunta_respondida.pregunta.opciones.get(pk=respuesta_pk)
        
        except ObjectDoesNotExist:
            raise Http404
		
        QuizUser.validar_intento(pregunta_respondida, opcion_selecionada)
        return redirect('resultado', pregunta_respondida.pk)

    else:
  
        pregunta = QuizUser.obtener_nuevas_preguntas()
        if pregunta is not None:
            QuizUser.crear_intentos(pregunta)

        context = {
            'pregunta':pregunta
        }

    return render(request, 'jugar/jugarPrueba.html', context)


def resultado_pregunta(request, pregunta_respondida_pk):
    respondida = get_object_or_404(PreguntasRespondidasTrivia, pk=pregunta_respondida_pk)

    context = {
        'respondida':respondida
    }

    return render(request, 'jugar/resultados.html', context)

def tablero(request):
    total_usuarios_quiz = QuizUsuarioTrivia.objects.order_by('-puntaje_total')[:10]
    contador = total_usuarios_quiz.count()

    context = {
        'usuario_quiz':total_usuarios_quiz,
        'contar_user':contador
    }

    return render(request, 'jugar/tablero.html', context)

@login_required
def jugar(request):
    trivias = Trivia.objects.all()

    context = {
        'trivias':trivias,
    }
    return render(request, 'jugar/jugar.html', context)



@login_required
def jugarTrivia(request, Trivia_id):

    if request.method == 'POST':
        
        trivias = Trivia.objects.get(id=Trivia_id)
        preguntas = Pregunta.objects.all()

        puntaje = 0
        incorrecta = 0
        correcta = 0
        total = 0
        count = 0
        
        for pregunta in preguntas:
            if pregunta.trivia.id == trivias.id: 
                opcion_seleccionada = request.POST.get(str(pregunta.pk))
                total += 1

                if opcion_seleccionada == pregunta.opcionCorrecta:
                    puntaje += 10
                    correcta +=1
                else:
                    incorrecta +=1

        percent = puntaje/(total*10) *100                    

        context = {
            'preguntas':preguntas,
            'trivias':trivias,
            'puntaje':puntaje,
            'incorrecta':incorrecta,
            'correcta':correcta,
            'total':total,
            'count':count,
            'percent':percent,
        }
        return render(request, 'TGApp/result.html', context)

    else:

        context = {
            'preguntas':Pregunta.objects.order_by('?'),
            'trivias':Trivia.objects.get(id=Trivia_id),
        }

        return render (request, 'jugar/jugarTrivia.html', context)
        
